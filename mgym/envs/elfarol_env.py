import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
import copy


class ElFarolEnv(mgym.MEnv):
    def __init__(self):
        self.n = None  # Set in reset function
        self.action_space = None  # Set in reset function
        self.observation_space = None
        self.nA = 2
        self.nS = 1
        self.WORD_FOR_ACTION = {0: 'STAY HOME',
                                1: 'GO TO BAR'}

    def reset(num_players=10):
        self.n = num_players
        self.action_space = spaces.Tuple(
            (spaces.Discrete(self.nA) for _ in self.n))
        self.observation_space = spaces.Discrete(1)

    def step(action):
        pass

    def render():
        pass
