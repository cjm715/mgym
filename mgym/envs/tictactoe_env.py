import gym
from gym import error, spaces, utils
from gym.utils import seeding


class TicTacToeEnv(gym.Env):
    """
    Simple TicTacToeEnv as toytext environment.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.shape = (3, 3)
        nS = 3**3
        nA = 9
        agents = {}

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        pass
