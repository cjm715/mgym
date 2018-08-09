import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
from mgym.envs import repeatedgame


class BattleOfTheSexesEnv(repeatedgame.RepeatedTwoPlayerGame):
    '''
    Repeated Battle Of The Sexes
    '''

    def __init__(self):
        word_for_action = {0: 'OPERA',
                           1: 'FOOTBALL'}
        utility_matrix = [[(3, 2), (0, 0)],
                          [(0, 0), (2, 3)]]

        super(BattleOfTheSexesEnv, self).__init__(
            utility_matrix, word_for_action=word_for_action)
