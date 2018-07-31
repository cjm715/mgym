import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
from mgym.envs import repeatedgame


class RockPaperScissorsEnv(repeatedgame.RepeatedTwoPlayerGame):
    '''
    Repeated Rock-Paper-Scissors
    '''

    def __init__(self):
        WORD_FOR_ACTION = {0: 'ROCK',
                           1: 'PAPER',
                           2: 'SCISSORS'}
        U = [[(0, 0), (-1, 1),  (1, -1)],
             [(1, -1),  (0, 0),  (-1, 1)],
             [(-1, 1), (1, -1),   (0, 0)]]

        super(RockPaperScissorsEnv, self).__init__(
            U, WORD_FOR_ACTION=WORD_FOR_ACTION)
