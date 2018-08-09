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
        word_for_action = {0: 'HEADS',
                           1: 'TAILS'}
        utility_matrix = [[(1, -1), (-1, 1)],
                          [(-1, 1), (1, -1)]]

        super(MatchingPenniesEnv, self).__init__(
            utility_matrix, word_for_action=word_for_action)
