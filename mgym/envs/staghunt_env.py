import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
from mgym.envs import repeatedgame


class StagHuntEnv(repeatedgame.RepeatedTwoPlayerGame):
    '''
    Repeated StageHunt
    '''

    def __init__(self):
        word_for_action = {0: 'STAG',
                           1: 'HARE'}
        utility_matrix = [[(2, 2), (0, 1)],
                          [(1, 0), (1, 1)]]

        super(StagHuntEnv, self).__init__(
            utility_matrix, word_for_action=word_for_action)
