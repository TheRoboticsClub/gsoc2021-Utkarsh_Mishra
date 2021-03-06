#!/usr/bin/env python

import pickle

import numpy as np
import torch
import torch.optim as optim

from DDPG.ddpg_step import ddpg_step
from models.policies import DDPGPolicy
from models.values import DDPGValue
from models.image_policies import DDPGPolicyImage
from models.image_values import DDPGValueImage
from utils.replay_memory import Memory
from utils.env_util import get_env_info, get_pixel_env_info
from utils.file_util import check_path
from utils.torch_util import device, FLOAT


class DDPG:
    def __init__(self,
                 env_id,
                 obs_type='pixel',
                 render=False,
                 num_process=1,
                 memory_size=1000000,
                 lr_p=1e-3,
                 lr_v=1e-3,
                 gamma=0.99,
                 polyak=0.995,
                 explore_size=10000,
                 step_per_iter=3000,
                 batch_size=100,
                 min_update_step=1000,
                 update_step=50,
                 action_noise=0.1,
                 seed=1,
                 model_path=None
                 ):
        self.env_id = env_id
        self.gamma = gamma
        self.polyak = polyak
        self.memory = Memory(memory_size)
        self.explore_size = explore_size
        self.step_per_iter = step_per_iter
        self.render = render
        self.num_process = num_process
        self.lr_p = lr_p
        self.lr_v = lr_v
        self.batch_size = batch_size
        self.min_update_step = min_update_step
        self.update_step = update_step
        self.action_noise = action_noise
        self.model_path = model_path
        self.seed = seed

        self.obs_type = obs_type

        self._init_model()

    def _init_model(self):
        """init model from parameters"""

        if self.obs_type == 'pixel':
            self.env, env_continuous, obs_shape, num_states, self.num_actions = get_pixel_env_info(self.env_id)

            assert env_continuous, "DDPG is only applicable to continuous environment !!!!"

            self.action_low, self.action_high = self.env.action_space.low[
                0], self.env.action_space.high[0]
            # seeding
            np.random.seed(self.seed)
            torch.manual_seed(self.seed)
            self.env.seed(self.seed)

            self.policy_net = DDPGPolicyImage(obs_shape, 32, 
                num_states, self.num_actions, self.action_high).to(device)
            self.policy_net_target = DDPGPolicyImage(obs_shape, 32,
                num_states, self.num_actions, self.action_high).to(device)

            self.value_net = DDPGValueImage(obs_shape, 32, num_states, self.num_actions).to(device)
            self.value_net_target = DDPGValueImage(obs_shape, 32, num_states, self.num_actions).to(device)
        else:
            self.env, env_continuous, num_states, self.num_actions = get_env_info(
                self.env_id)
            assert env_continuous, "DDPG is only applicable to continuous environment !!!!"

            self.action_low, self.action_high = self.env.action_space.low[
                0], self.env.action_space.high[0]
            # seeding
            np.random.seed(self.seed)
            torch.manual_seed(self.seed)
            self.env.seed(self.seed)

            self.policy_net = DDPGPolicy(
                num_states, self.num_actions, self.action_high).to(device)
            self.policy_net_target = DDPGPolicy(
                num_states, self.num_actions, self.action_high).to(device)

            self.value_net = DDPGValue(num_states, self.num_actions).to(device)
            self.value_net_target = DDPGValue(num_states, self.num_actions).to(device)

        if self.model_path:
            print("Loading Saved Model {}_ddpg.p".format(self.env_id))
            self.policy_net, self.value_net, self.running_state = pickle.load(
                open('{}/{}_ddpg.p'.format(self.model_path, self.env_id), "rb"))

        self.policy_net_target.load_state_dict(self.policy_net.state_dict())
        self.value_net_target.load_state_dict(self.value_net.state_dict())

        self.optimizer_p = optim.Adam(
            self.policy_net.parameters(), lr=self.lr_p)
        self.optimizer_v = optim.Adam(
            self.value_net.parameters(), lr=self.lr_v)

    def choose_action(self, image, state, noise_scale):
        """select action"""
        image = FLOAT(image).unsqueeze(0).to(device)
        state = FLOAT(state).unsqueeze(0).to(device)
        with torch.no_grad():
            action, log_prob = self.policy_net.get_action_log_prob(image, state)
        action = action.cpu().numpy()[0]
        # add noise
        noise = noise_scale * np.random.randn(self.num_actions)
        action += noise
        action = np.clip(action, -self.action_high, self.action_high)
        return action 

    def eval(self, i_iter, render=False):
        """evaluate model"""
        image, state = self.env.reset()
        test_reward = 0
        while True:
            if render:
                self.env.render()
            action = self.choose_action(image, state, 0)
            states, reward, done, _ = self.env.step(action)
            image, state = states

            test_reward += reward
            if done:
                break
        print(f"Iter: {i_iter}, test Reward: {test_reward}")

    def learn(self, writer, i_iter):
        """interact"""
        global_steps = (i_iter - 1) * self.step_per_iter
        log = dict()
        num_steps = 0
        num_episodes = 0
        total_reward = 0
        min_episode_reward = float('inf')
        max_episode_reward = float('-inf')

        while num_steps < self.step_per_iter:
            image, state = self.env.reset()
            episode_reward = 0

            for t in range(10000):

                if self.render:
                    self.env.render()

                if global_steps < self.explore_size:  # explore
                    action = self.env.action_space.sample()
                else:  # action with noise
                    action = self.choose_action(image, state, self.action_noise)

                next_states, reward, done, _ = self.env.step(action)
                next_image, next_state = next_states
                mask = 0 if done else 1
                # ('state', 'action', 'reward', 'next_state', 'mask', 'log_prob')
                self.memory.push(image, state, action, reward, next_image, next_state, mask, None)

                episode_reward += reward
                global_steps += 1
                num_steps += 1

                if global_steps >= self.min_update_step and global_steps % self.update_step == 0:
                    for _ in range(self.update_step):
                        batch = self.memory.sample(
                            self.batch_size)  # random sample batch
                        self.update(batch)

                if done or num_steps >= self.step_per_iter:
                    break

                state = next_state

            num_episodes += 1
            total_reward += episode_reward
            min_episode_reward = min(episode_reward, min_episode_reward)
            max_episode_reward = max(episode_reward, max_episode_reward)

        log['num_steps'] = num_steps
        log['num_episodes'] = num_episodes
        log['total_reward'] = total_reward
        log['avg_reward'] = total_reward / num_episodes
        log['max_episode_reward'] = max_episode_reward
        log['min_episode_reward'] = min_episode_reward

        print(f"Iter: {i_iter}, num steps: {log['num_steps']}, total reward: {log['total_reward']: .4f}, "
              f"min reward: {log['min_episode_reward']: .4f}, max reward: {log['max_episode_reward']: .4f}, "
              f"average reward: {log['avg_reward']: .4f}")

        # record reward information
        writer.add_scalar("total reward", log['total_reward'], i_iter)
        writer.add_scalar("average reward", log['avg_reward'], i_iter)
        writer.add_scalar("min reward", log['min_episode_reward'], i_iter)
        writer.add_scalar("max reward", log['max_episode_reward'], i_iter)
        writer.add_scalar("num steps", log['num_steps'], i_iter)

    def update(self, batch):
        """learn model"""
        batch_image = FLOAT(batch.image).to(device)
        batch_state = FLOAT(batch.state).to(device)
        batch_action = FLOAT(batch.action).to(device)
        batch_reward = FLOAT(batch.reward).to(device)
        batch_next_image = FLOAT(batch.next_image).to(device)
        batch_next_state = FLOAT(batch.next_state).to(device)
        batch_mask = FLOAT(batch.mask).to(device)

        # update by DDPG
        alg_step_stats = ddpg_step(self.policy_net, self.policy_net_target, self.value_net, self.value_net_target, self.optimizer_p,
                                   self.optimizer_v, batch_image, batch_state, batch_action, batch_reward, batch_next_image, batch_next_state, batch_mask,
                                   self.gamma, self.polyak)

    def save(self, save_path):
        """save model"""
        check_path(save_path)
        pickle.dump((self.policy_net, self.value_net),
                    open('{}/{}_ddpg.p'.format(save_path, self.env_id), 'wb'))
