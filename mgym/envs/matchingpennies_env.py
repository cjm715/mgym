import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
from mgym.envs import repeatedgame


class MatchingPenniesEnv(repeatedgame.RepeatedTwoPlayerGame):
    '''
    Repeated Matching Pennies
    '''

    def __init__(self):
        WORD_FOR_ACTION = {0: 'HEADS',
                           1: 'TAILS'}
        U = [[(1, -1), (-1, 1)],
             [(-1, 1), (1, -1)]]

        super(MatchingPenniesEnv, self).__init__(
            U, WORD_FOR_ACTION=WORD_FOR_ACTION)
