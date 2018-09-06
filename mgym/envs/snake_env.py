"""Snake environment"""
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
import copy

screen_height = 100
screen_width = 100


class SnakeEnv(mgym.MEnv):
    """ Multi-agent version of classic Nokia snake game.

    This environment is proposed in the OpenAI's request-for-research page [RR]. This request is inspired by
    slither.io [SL].

    References
    ---------
    .. [RR] https://blog.openai.com/requests-for-research-2/
    .. [SL] http://slither.io/

    """

    def __init__(self):
        self.N = None  # set in reset function

    def reset(self, N):
        self.N = N
        self.nA = 5
        self.screen_shape = (screen_height, screen_width)
        self.observation_space = spaces.Box(low=0, high=(self.N + 1), shape=(
            screen_height, screen_width), dtype=np.uint8)
        self.action_space = spaces.Tuple(
            [spaces.Discrete(self.nA) for _ in range(self.N)])
        self.state = np.zeros(self.screen_shape)
