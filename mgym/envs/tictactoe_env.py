import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import gym.spaces

EMPTY = 0
X = 1
O = 2

LOOK_UP_SYM = {0: ' ',
               1: 'X',
               2: 'O'}


class TicTacToeEnv(gym.Env):
    """
    Simple TicTacToeEnv as toytext environment.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, ordering=None):
        self.shape = (3, 3)
        self.n = 2  # number of agents
        self.nA = 9  # number of actions per player
        self.nS = 3**9  # number of observations per player
        self.action_space = []
        self.observation_space = []
        self.grid = None
        self.whos_up_list = []

        for i in range(self.n):
            ind_action_space = spaces.Discrete(self.nA)
            self.action_space.append(ind_action_space)
            ind_observation_space = spaces.Discrete(self.nS)
            self.observation_space.append(ind_observation_space)

        self.ordering = 'cyclic'

    def step(self, action):

        observation_list = [None for _ in range(self.n)]
        reward_list = [None for _ in range(self.n)]
        done_list = [False for _ in range(self.n)]
        info_list = [None for _ in range(self.n)]

        observation_list[self.whos_up] = self._observe_grid()

        if self._game_over():
            reward_list[self.whos_up] = 0
            done_list = [True for _ in range(self.n)]

        return observation_list, reward_list, done_list, info_list

    def reset(self):
        self.grid = np.zeros(self.shape)
        return self._observe_grid()

    def render(self, mode='human', close=False):
        for i in range(3):
            row_str = ""
            for j in range(3):
                row_str += ("| " + LOOK_UP_SYM[self.grid[i, j]] + " ")
            row_str += "|\n"
            print(row_str)

    def _observe_grid(self):
        s = 0
        for i in range(3):
            for j in range(3):
                s = self.grid[i, j] + 3 * s
        return s


class TicTacToeAgent(object):
    def __init__(self, observation_space, action_space):
        # Set these in ALL subclasses
        action_space = observation_space
        observation_space = action_space

    def act(self, observation, reward, done):
        raise NotImplementedError
