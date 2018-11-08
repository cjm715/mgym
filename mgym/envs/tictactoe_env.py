import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
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

    The action space is spaces.Tuple((spaces.Discrete(self.n),spaces.Discrete(self.nA)))
    where self.n is the number of agents (=2) and self.nA is the number of actions (=9).
    The first index of the tuple represents which agent is acting and the second
    index is its action.

    The oberservation space is spaces.Tuple((spaces.Discrete(self.n),spaces.Discrete(self.nA)))
    where self.n is the number of agents (=2) and self.nS is the number of board positions (=3**9).
    The first index of the tuple represents which agent is acting next and the second
    index is the current state of the game. It is fully observable to both players.

    Example
    -------

    >>> import gym
    >>> import mgym
    >>> import random
    >>>
    >>> env = gym.make('TicTacToe-v0')
    >>> fullobs = env.reset()
    >>> i = 0
    >>> while True:
    ...     print('Player O ') if fullobs[0] else print('Player X')
    ...     a = random.choice(env.get_available_actions())
    ...     fullobs,rewards,done,_ = env.step(a)
    ...     env.render()
    ...     if done:
    ...         break


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
        won, _ = self._agent_won()

        if won:
            reward_list = [0 for _ in range(self.n)]
            reward_list[self.active_agent] = 1
            done = True
            return tuple([self.active_agent, observation]), tuple(reward_list), done, {}

        active_agent_old = self.active_agent
        self.active_agent = int((self.active_agent + 1) % 2)

        if self._no_available_actions():
            reward_list = [0 for _ in range(self.n)]
            done = True
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
                s = (self.grid[i, j] + 1) + 3 * s
        # return int(s)
        return self.grid

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
