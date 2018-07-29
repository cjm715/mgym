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
        self.action_space = spaces.Tuple((spaces.Discrete(self.n),
                                          spaces.Discrete(self.nA)))
        self.observation_space = spaces.Tuple((spaces.Discrete(self.n),
                                               spaces.Discrete(self.nS)))
        self.grid = None
        self.active_agent = None
        self.agent_sym = [X, O]

    def step(self, action_tuple):

        self._update_grid(action_tuple)
        observation = self._observe_grid()
        won, who_won = self._agent_won()

        if won:
            reward_list = [0 for _ in range(self.n)]
            reward_list[self.active_agent] = 1
            done = True
            if who_won == 0:
                print('X WON!')
            elif who_won == 1:
                print('O WON!')
            return tuple([self.active_agent, observation]), tuple(reward_list), done, {}

        active_agent_old = self.active_agent
        self.active_agent = int((self.active_agent + 1) % 2)

        if self._no_available_actions():
            reward_list = [0 for _ in range(self.n)]
            done = True
            print('DRAW')
            return tuple([active_agent_old, observation]), tuple(reward_list), done, {}

        observation_list = [self.active_agent, observation]
        reward_list = [0 for _ in range(self.n)]
        done = False
        return tuple(observation_list), tuple(reward_list), done, {}

    def reset(self):
        self.grid = np.zeros(self.shape)
        self.active_agent = int(0)
        observation = self._observe_grid()
        observation_list = [self.active_agent, observation]
        observation_tuple = tuple(observation_list)
        return observation_tuple

    def render(self, mode='human', close=False):
        #print('Player O ') if self.active_agent else print('Player X')
        for i in range(3):
            row_str = ""
            for j in range(3):
                row_str += ("| " + LOOK_UP_SYM[self.grid[i, j]] + " ")
            row_str += "|\n"
            print(row_str)

    def get_available_actions(self):
        available_actions = []
        for potential_action in range(self.nA):
            j, k = self._action_to_grid_indices(potential_action)
            if self.grid[j, k] == EMPTY:
                available_actions.append((self.active_agent, potential_action))

        return available_actions

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
        agent = action_tuple[0]
        action = action_tuple[1]
        assert agent == self.active_agent
        j, k = self._action_to_grid_indices(action)
        assert self.grid[j, k] == EMPTY
        self.grid[j, k] = self.agent_sym[agent]

    def _agent_won(self):
        # check for 3 in a row
        for mask in MASK_LIST:
            if np.sum(self.grid * mask) == 3:
                return True, 0
            elif np.sum(self.grid * mask) == -3:
                return True, 1
        return False, None

    def _no_available_actions(self):
        return not self.get_available_actions()
