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
        WORD_FOR_ACTION = {0: 'STAG',
                           1: 'HARE'}
        U = [[(2, 2), (0, 1)],
             [(1, 0), (1, 1)]])

        super(RockPaperScissorsEnv, self).__init__(
            U, WORD_FOR_ACTION = WORD_FOR_ACTION)
