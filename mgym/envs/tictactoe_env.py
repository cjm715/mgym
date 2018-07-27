import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import gym.spaces

O = -1
EMPTY = 0
X = 1

LOOK_UP_SYM = {-1: 'O',
               0: ' ',
               1: 'X'
               }

MASK_LIST = [
    np.array([[1, 0, 0],
              [0, 1, 0],
              [0, 0, 1]]),
    np.array([[0, 0, 1],
              [0, 1, 0],
              [1, 0, 0]]),
    np.array([[1, 1, 1],
              [0, 0, 0],
              [0, 0, 0]]),
    np.array([[0, 0, 0],
              [1, 1, 1],
              [0, 0, 0]]),
    np.array([[0, 0, 0],
              [0, 0, 0],
              [1, 1, 1]]),
    np.array([[1, 0, 0],
              [1, 0, 0],
              [1, 0, 0]]),
    np.array([[0, 1, 0],
              [0, 1, 0],
              [0, 1, 0]]),
    np.array([[0, 0, 1],
              [0, 0, 1],
              [0, 0, 1]]),
]


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
        self.active_agent = None
        self.agent_sym = [X, O]

        for i in range(self.n):
            ind_action_space = spaces.Discrete(self.nA)
            self.action_space.append(ind_action_space)
            ind_observation_space = spaces.Discrete(self.nS)
            self.observation_space.append(ind_observation_space)

    def step(self, action_list):

        self._update_grid(action_list)

        if self._game_over():
            observation = self._observe_grid()
            observation_list = [observation for _ in range(self.n)]
            reward_list = [0 for _ in range(self.n)]
            reward_list[self.active_agent] = 1
            done_list = [True for _ in range(self.n)]
        else:
            observation = self._observe_grid()
            observation_list = [observation for _ in range(self.n)]
            reward_list = [0 for _ in range(self.n)]
            done_list = [False for _ in range(self.n)]

        self.active_agent = (self.active_agent + 1) % 2
        return observation_list, reward_list, done_list, self.active_agent

    def reset(self):
        self.grid = np.zeros(self.shape)
        self.active_agent = 0
        return self._observe_grid(), self.active_agent

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

    def _action_to_grid_indices(self, action):
        i = int(action // 3)
        j = int(action % 3)
        return i, j

    def _update_grid(self, action_list):

        for i, action in enumerate(action_list):
            if not (action == None):
                j, k = self._action_to_grid_indices(action)
                if self.grid[j, k] == EMPTY:
                    self.grid[j, k] = self.agent_sym[i]

    def _game_over(self):
        # check for 3 in a row
        for mask in MASK_LIST:
            if np.sum(self.grid * mask) == 3:
                print('X WON!')
                return True
            elif np.sum(self.grid * mask) == -3:
                print('O WON!')
                return True
        return False


class TicTacToeAgent(object):
    def __init__(self, observation_space, action_space):
        # Set these in ALL subclasses
        action_space = observation_space
        observation_space = action_space

    def act(self, observation, reward, done):
        raise NotImplementedError
