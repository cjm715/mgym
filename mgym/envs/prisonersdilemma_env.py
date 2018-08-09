import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
import copy
from mgym.envs import repeatedgame


class PrisonersDilemmaEnv(repeatedgame.RepeatedTwoPlayerGame):
    '''
    Repeated Prisoners Dilemma
    '''

    def __init__(self):
        word_for_action = {0: 'COOPERATE',
                           1: 'DEFECT'}
        utility_matrix = [[(3, 3), (0, 5)],
                          [(5, 0), (1, 1)]]

        super(PrisonersDilemmaEnv, self).__init__(
            utility_matrix, word_for_action=word_for_action)
