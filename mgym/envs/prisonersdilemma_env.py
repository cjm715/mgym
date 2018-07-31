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
        WORD_FOR_ACTION = {0: 'COOPERATE',
                           1: 'DEFECT'}
        U = [[(3, 3), (0, 5)],
             [(5, 0), (1, 1)]]

        super(PrisonersDilemmaEnv, self).__init__(
            U, WORD_FOR_ACTION=WORD_FOR_ACTION)
