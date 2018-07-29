import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import gym.spaces
import mgym
O = -1
EMPTY = 0
X = 1

NO_AGENT = -1

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


class TicTacToeEnv(mgym.MEnv):
    """
    Simple TicTacToeEnv as toytext environment.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.shape = (3, 3)
        self.n = 2  # number of agents
        self.nA = 9  # number of actions per player
        self.nS = 3**9  # number of observations per player
        self.action_space = spaces.Tuple((spaces.Discrete(self.nA),
                                          spaces.Discrete(self.nA)))
        self.observation_space = spaces.Tuple((spaces.Discrete(self.n),
                                               spaces.Discrete(self.nS),
                                               spaces.Discrete(self.nS)))
        self.grid = None
        self.active_agent = None
        self.agent_sym = [X, O]

    def step(self, action_tuple):

        if not self._action_is_valid(action_tuple):
            observation = self._observe_grid()
            observation_list = [self.active_agent]
            for _ in range(self.n):
                observation_list.append(observation)

            reward_list = [0 for _ in range(self.n)]
            done = True
        else:
            self._update_grid(action_tuple)

            if self._game_over():
                observation = self._observe_grid()
                observation_list = [self.active_agent]
                for _ in range(self.n):
                    observation_list.append(observation)
                reward_list = [0 for _ in range(self.n)]
                reward_list[self.active_agent] = 1
                done = True
            else:
                observation = self._observe_grid()
                self.active_agent = int((self.active_agent + 1) % 2)
                observation_list = [self.active_agent]
                for _ in range(self.n):
                    observation_list.append(observation)
                reward_list = [0 for _ in range(self.n)]
                done = False

        return tuple(observation_list), tuple(reward_list), done, {}

    def reset(self):
        self.grid = np.zeros(self.shape)
        self.active_agent = int(0)
        observation = self._observe_grid()
        observation_list = [self.active_agent]
        for _ in range(self.n):
            observation_list.append(observation)
        observation_tuple = tuple(observation_list)
        return observation_tuple

    def render(self, mode='human', close=False):
        for i in range(3):
            row_str = ""
            for j in range(3):
                row_str += ("| " + LOOK_UP_SYM[self.grid[i, j]] + " ")
            row_str += "|\n"
            print(row_str)

    def _action_is_valid(self, action_tuple):
        for i, action in enumerate(action_tuple):
            if i != self.active_agent:
                assert None == action_tuple[i]
            else:
                assert not (None == action_tuple[i])
                j, k = self._action_to_grid_indices(action)
                assert self.grid[j, k] == EMPTY

        return True

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

    def _update_grid(self, action_tuple):
        for i, action in enumerate(action_tuple):
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

    def available_actions(self, state):
        pass
