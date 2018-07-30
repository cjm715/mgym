import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
import copy
from mgym.envs import repeatedgame


class PrisonersDilemmaEnv(repeatedgame.RepeatedTwoPlayerSymmetricGame):
    '''
    Repeated Prisoners Dilemma
    '''

    def __init__(self):
        WORD_FOR_ACTION = {0: 'COOPERATE',
                           1: 'DEFECT'}
        U = np.array([[3, 0],
                      [5, 1]])

        super(PrisonersDilemmaEnv, self).__init__(
            U, WORD_FOR_ACTION=WORD_FOR_ACTION)
