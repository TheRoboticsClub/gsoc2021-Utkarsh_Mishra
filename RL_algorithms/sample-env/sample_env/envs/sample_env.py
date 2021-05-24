import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np
import cv2

class SampleEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):

        super(SampleEnv, self).__init__()

        self.image_height = 32
        self.image_width = 32
        self.num_channels = 1
        self.frame_stack = 3

        self.observation_shape = (self.frame_stack*self.num_channels,
                                self.image_height, 
                                self.image_width)
        self.observation_space = spaces.Box(low = np.zeros(self.observation_shape), 
                                            high = np.ones(self.observation_shape),
                                            dtype = np.float16)

        self.state_dim = 2      
        self.action_dim = 2

        self.action_space = spaces.Box(low = -np.ones(self.action_dim), 
                                        high = np.ones(self.action_dim),
                                        dtype = np.float16)

        self.curr_state = np.array([0, 0])
        self.w_transition = 0.6
    
    def step(self, action):

        assert action.shape[0] == self.action_dim

        curr_state = self.curr_state
        new_state = curr_state + self.w_transition*(action - curr_state)

        self.curr_state = new_state

        next_obs = self._get_obs()
        reward = self._get_reward()
        done = self._get_done()

        return next_obs, reward, done, {}

    def _get_obs(self):

        self.canvas = np.random.rand(self.frame_stack*self.num_channels,
                                    self.image_height, 
                                    self.image_width)

        return (self.canvas, self.curr_state)

    def _get_reward(self):

        reward = np.linalg.norm(self.curr_state)

        return reward

    def _get_done(self):

        return False
    
    def reset(self):

        self.curr_state = np.array([0, 0])

        return self._get_obs()

    def render(self, mode = "human"):
        assert mode in ["human", "rgb_array"], "Invalid mode, must be either \"human\" or \"rgb_array\""
        if mode == "human":
            cv2.imshow("Game", self.canvas)
            cv2.waitKey(10)
        
        elif mode == "rgb_array":
            return self.canvas
        
    def close(self):
        cv2.destroyAllWindows()

class SampleEnvDiscrete(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):

        super(SampleEnvDiscrete, self).__init__()

        self.image_height = 32
        self.image_width = 32
        self.num_channels = 1
        self.frame_stack = 3

        self.observation_shape = (self.frame_stack*self.num_channels,
                                self.image_height, 
                                self.image_width)
        self.observation_space = spaces.Box(low = np.zeros(self.observation_shape), 
                                            high = np.ones(self.observation_shape),
                                            dtype = np.float16)

        self.state_dim = 2      
        self.action_dim = 2

        self.action_space = spaces.Discrete(self.action_dim)

        self.curr_state = np.array([0, 0])
        self.w_transition = 0.6
    
    def step(self, action):

        actions = np.array([action]*self.action_dim)

        curr_state = self.curr_state
        new_state = curr_state + self.w_transition*(action - curr_state)

        self.curr_state = new_state

        next_obs = self._get_obs()
        reward = self._get_reward()
        done = self._get_done()

        return next_obs, reward, done, {}

    def _get_obs(self):

        self.canvas = np.random.rand(self.frame_stack*self.num_channels,
                                    self.image_height, 
                                    self.image_width)

        return (self.canvas, self.curr_state)

    def _get_reward(self):

        reward = np.linalg.norm(self.curr_state)

        return reward

    def _get_done(self):

        return False
    
    def reset(self):

        self.curr_state = np.array([0, 0])

        return self._get_obs()

    def render(self, mode = "human"):
        assert mode in ["human", "rgb_array"], "Invalid mode, must be either \"human\" or \"rgb_array\""
        if mode == "human":
            cv2.imshow("Game", self.canvas)
            cv2.waitKey(10)
        
        elif mode == "rgb_array":
            return self.canvas
        
    def close(self):
        cv2.destroyAllWindows()