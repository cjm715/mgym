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
        word_for_action = {0: 'ROCK',
                           1: 'PAPER',
                           2: 'SCISSORS'}
        utility_matrix = [[(0, 0), (-1, 1),  (1, -1)],
                          [(1, -1),  (0, 0),  (-1, 1)],
                          [(-1, 1), (1, -1),   (0, 0)]]

        super(RockPaperScissorsEnv, self).__init__(
            utility_matrix, word_for_action=word_for_action)
