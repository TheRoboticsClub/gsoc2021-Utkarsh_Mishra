#!/usr/bin/env python

import math
import pickle

import torch
import torch.optim as optim

from models.policies import PPOPolicy, DiscretePolicy
from models.values import PPOValue
from models.image_policies import PPOPolicyImage, DiscretePolicyImage
from models.image_values import PPOValueImage
from PPO.ppo_step import ppo_step
from utils.GAE import estimate_advantages
from utils.MemoryCollector import MemoryCollector
from utils.env_util import get_env_info, get_pixel_env_info
from utils.file_util import check_path
from utils.torch_util import device, FLOAT


class PPO:
    def __init__(self,
                 env_id,
                 obs_type='pixel',
                 render=False,
                 num_process=4,
                 min_batch_size=2048,
                 lr_p=3e-4,
                 lr_v=3e-4,
                 gamma=0.99,
                 tau=0.95,
                 clip_epsilon=0.2,
                 ppo_epochs=10,
                 ppo_mini_batch_size=64,
                 seed=1,
                 model_path=None
                 ):
        self.env_id = env_id
        self.gamma = gamma
        self.tau = tau
        self.ppo_epochs = ppo_epochs
        self.ppo_mini_batch_size = ppo_mini_batch_size
        self.clip_epsilon = clip_epsilon
        self.render = render
        self.num_process = num_process
        self.lr_p = lr_p
        self.lr_v = lr_v
        self.min_batch_size = min_batch_size
        self.obs_type = obs_type

        self.model_path = model_path
        self.seed = seed
        self._init_model()

    def _init_model(self):
        """init model from parameters"""
        # seeding
        torch.manual_seed(self.seed)
        self.env.seed(self.seed)
        if self.obs_type == 'pixel':
            self.env, env_continuous, obs_shape, num_states, num_actions = get_pixel_env_info(self.env_id)

            if env_continuous:
                self.policy_net = PPOPolicyImage(obs_shape, 32, num_states, num_actions).to(device)
            else:
                self.policy_net = DiscretePolicyImage(obs_shape, 32, num_states, num_actions).to(device)

            self.value_net = PPOValueImage(obs_shape, 32, num_states).to(device)
        else:
            self.env, env_continuous, num_states, num_actions = get_env_info(self.env_id)

            if env_continuous:
                self.policy_net = PPOPolicy(num_states[0], num_actions).to(device)
            else:
                self.policy_net = DiscretePolicy(
                    num_states[0], num_actions).to(device)

            self.value_net = PPOValue(num_states[0]).to(device)

        if self.model_path:
            print("Loading Saved Model {}_ppo.p".format(self.env_id))
            self.policy_net, self.value_net = pickle.load(
                open('{}/{}_ppo.p'.format(self.model_path, self.env_id), "rb"))

        self.collector = MemoryCollector(self.env, self.policy_net, render=self.render,
                                         num_process=self.num_process)

        self.optimizer_p = optim.Adam(
            self.policy_net.parameters(), lr=self.lr_p)
        self.optimizer_v = optim.Adam(
            self.value_net.parameters(), lr=self.lr_v)

    def choose_action(self, image, state):
        """select action"""
        image = FLOAT(image).unsqueeze(0).to(device)
        state = FLOAT(state).unsqueeze(0).to(device)
        with torch.no_grad():
            action, log_prob = self.policy_net.get_action_log_prob(image, state)
        
        action = action.cpu().numpy()[0]
        return action

    def eval(self, i_iter, render=False):
        image, state = self.env.reset()
        test_reward = 0
        while True:
            if render:
                self.env.render()
            action = self.choose_action(image, state)
            states, reward, done, _ = self.env.step(action)
            image, state = states

            test_reward += reward
            if done:
                break
        print(f"Iter: {i_iter}, test Reward: {test_reward}")
        self.env.close()

    def learn(self, writer, i_iter):
        """learn model"""
        memory, log = self.collector.collect_samples(self.min_batch_size)

        print(f"Iter: {i_iter}, num steps: {log['num_steps']}, total reward: {log['total_reward']: .4f}, "
              f"min reward: {log['min_episode_reward']: .4f}, max reward: {log['max_episode_reward']: .4f}, "
              f"average reward: {log['avg_reward']: .4f}, sample time: {log['sample_time']: .4f}")

        # record reward information
        writer.add_scalar("total reward", log['total_reward'], i_iter)
        writer.add_scalar("average reward", log['avg_reward'], i_iter)
        writer.add_scalar("min reward", log['min_episode_reward'], i_iter)
        writer.add_scalar("max reward", log['max_episode_reward'], i_iter)
        writer.add_scalar("num steps", log['num_steps'], i_iter)

        batch = memory.sample()  # sample all items in memory
        #  ('state', 'action', 'reward', 'next_state', 'mask', 'log_prob')
        batch_image = FLOAT(batch.image).to(device)
        batch_state = FLOAT(batch.state).to(device)
        batch_action = FLOAT(batch.action).to(device)
        batch_reward = FLOAT(batch.reward).to(device)
        batch_mask = FLOAT(batch.mask).to(device)
        batch_log_prob = FLOAT(batch.log_prob).to(device)

        with torch.no_grad():
            batch_value = self.value_net(batch_image, batch_state)

        batch_advantage, batch_return = estimate_advantages(batch_reward, batch_mask, batch_value, self.gamma,
                                                            self.tau)

        alg_step_stats = {}
        if self.ppo_mini_batch_size:
            batch_size = batch_state.shape[0]
            mini_batch_num = int(
                math.ceil(batch_size / self.ppo_mini_batch_size))

            # update with mini-batch
            for _ in range(self.ppo_epochs):
                index = torch.randperm(batch_size)

                for i in range(mini_batch_num):
                    ind = index[
                        slice(i * self.ppo_mini_batch_size, min(batch_size, (i + 1) * self.ppo_mini_batch_size))]
                    image, state, action, returns, advantages, old_log_pis = batch_image[ind], batch_state[ind], batch_action[ind], \
                        batch_return[
                        ind], batch_advantage[ind], \
                        batch_log_prob[
                        ind]

                    alg_step_stats = ppo_step(self.policy_net, self.value_net, self.optimizer_p, self.optimizer_v,
                                              1,
                                              image,
                                              state,
                                              action, returns, advantages, old_log_pis, self.clip_epsilon,
                                              1e-3)
        else:
            for _ in range(self.ppo_epochs):
                alg_step_stats = ppo_step(self.policy_net, self.value_net, self.optimizer_p, self.optimizer_v, 1,
                                          batch_image, batch_state, batch_action, batch_return, batch_advantage, batch_log_prob,
                                          self.clip_epsilon,
                                          1e-3)

        return alg_step_stats

    def save(self, save_path):
        """save model"""
        check_path(save_path)
        pickle.dump((self.policy_net, self.value_net),
                    open('{}/{}_ppo.p'.format(save_path, self.env_id), 'wb'))
