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
        WORD_FOR_ACTION = {0: 'OPERA',
                           1: 'FOOTBALL'}
        U = [[(3, 2), (0, 0)],
             [(0, 2), (2, 3)]]

        super(RockPaperScissorsEnv, self).__init__(
            U, WORD_FOR_ACTION=WORD_FOR_ACTION)
