#!/usr/bin/env python
# Created at 2020/3/3
import pickle

import numpy as np
import torch
import torch.optim as optim

from DQN.dqn_step import dqn_step
from models.policies import QPolicy
from models.image_policies import QPolicyImage
from utils.replay_memory import Memory
from utils.env_util import get_env_info, get_pixel_env_info
from utils.file_util import check_path
from utils.torch_util import device, FLOAT, LONG


class DQN:
    def __init__(self,
                 env_id,
                 obs_type='pixel',
                 render=False,
                 num_process=1,
                 memory_size=1000000,
                 explore_size=10000,
                 step_per_iter=3000,
                 lr_q=1e-3,
                 gamma=0.99,
                 batch_size=128,
                 min_update_step=1000,
                 epsilon=0.90,
                 update_target_gap=50,
                 seed=1,
                 model_path=None
                 ):
        self.env_id = env_id
        self.render = render
        self.num_process = num_process
        self.memory = Memory(size=memory_size)
        self.explore_size = explore_size
        self.step_per_iter = step_per_iter
        self.lr_q = lr_q
        self.gamma = gamma
        self.batch_size = batch_size
        self.min_update_step = min_update_step
        self.update_target_gap = update_target_gap
        self.epsilon = epsilon
        self.seed = seed
        self.model_path = model_path
        self.obs_type = obs_type

        self._init_model()

    def _init_model(self):
        """init model from parameters"""

        if self.obs_type == 'pixel':
            self.env, env_continuous, obs_shape, num_states, self.num_actions = get_pixel_env_info(self.env_id)
            assert not env_continuous, "DQN is only applicable to discontinuous environment !!!!"

            # seeding
            np.random.seed(self.seed)
            torch.manual_seed(self.seed)
            self.env.seed(self.seed)

            # initialize networks
            self.value_net = QPolicyImage(obs_shape, 32, num_states, self.num_actions).to(device)
            self.value_net_target = QPolicyImage(obs_shape, 32, num_states, self.num_actions).to(device)
        else:
            self.env, env_continuous, num_states, self.num_actions = get_env_info(
                self.env_id)
            assert not env_continuous, "DQN is only applicable to discontinuous environment !!!!"

            # seeding
            np.random.seed(self.seed)
            torch.manual_seed(self.seed)
            self.env.seed(self.seed)

            # initialize networks
            self.value_net = QPolicy(num_states, self.num_actions).to(device)
            self.value_net_target = QPolicy(num_states, self.num_actions).to(device)

        # load model if necessary
        if self.model_path:
            print("Loading Saved Model {}_dqn.p".format(self.env_id))
            self.value_net = pickle.load(
                open('{}/{}_dqn.p'.format(self.model_path, self.env_id), "rb"))

        self.value_net_target.load_state_dict(self.value_net.state_dict())

        self.optimizer = optim.Adam(self.value_net.parameters(), lr=self.lr_q)

    def choose_action(self, image, state):
        image = FLOAT(image).unsqueeze(0).to(device)
        state = FLOAT(state).unsqueeze(0).to(device)
        if np.random.uniform() <= self.epsilon:
            with torch.no_grad():
                action = self.value_net.get_action(image, state)
            action = action.cpu().numpy()[0]
        else:  # choose action greedy
            action = np.random.randint(0, self.num_actions)
        return action

    def eval(self, i_iter, render=False):
        """evaluate model"""
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
                else:  # choose according to target net
                    action = self.choose_action(image, state)

                next_states, reward, done, _ = self.env.step(action)
                next_image, next_state = next_states
                mask = 0 if done else 1
                # ('state', 'action', 'reward', 'next_state', 'mask', 'log_prob')
                self.memory.push(image, state, action, reward, next_image, next_state, mask, None)

                episode_reward += reward
                global_steps += 1
                num_steps += 1

                if global_steps >= self.min_update_step:
                    batch = self.memory.sample(
                        self.batch_size)  # random sample batch
                    self.update(batch)

                if global_steps % self.update_target_gap == 0:
                    self.value_net_target.load_state_dict(
                        self.value_net.state_dict())

                if done or num_steps >= self.step_per_iter:
                    break

                state = next_state

            num_episodes += 1
            total_reward += episode_reward
            min_episode_reward = min(episode_reward, min_episode_reward)
            max_episode_reward = max(episode_reward, max_episode_reward)

        self.env.close()

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
        batch_image = FLOAT(batch.image).to(device)
        batch_state = FLOAT(batch.state).to(device)
        batch_action = FLOAT(batch.action).to(device)
        batch_reward = FLOAT(batch.reward).to(device)
        batch_next_image = FLOAT(batch.next_image).to(device)
        batch_next_state = FLOAT(batch.next_state).to(device)
        batch_mask = FLOAT(batch.mask).to(device)

        alg_step_stats = dqn_step(self.value_net, self.optimizer, self.value_net_target, batch_image, batch_state, batch_action,
                                  batch_reward, batch_next_image, batch_next_state, batch_mask, self.gamma)

    def save(self, save_path):
        """save model"""
        check_path(save_path)
        pickle.dump((self.value_net),
                    open('{}/{}_dqn.p'.format(save_path, self.env_id), 'wb'))
