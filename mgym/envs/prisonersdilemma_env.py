import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
import copy

COOPERATE = 0
DEFECT = 1
WORD_FOR_ACTION = {0: 'COOPERATE',
                   1: 'DEFECT'}


class PrisonersDilemmaEnv(mgym.MEnv):
    def __init__(self):
        self.n = 2
        self.nA = 2
        self.nS = 1
        self.m = None  # number of iterations
        self.iteration_number = 0
        self.record_outcome = None
        self.action_space = spaces.Tuple(
            (spaces.Discrete(self.nA), spaces.Discrete(self.nA)))
        self.observation_space = spaces.Discrete(self.nS)

    def reset(self, total_iterations=100):
        self.iteration_number = 0
        self.record_outcome = None
        self.m = total_iterations
        return 0

    def step(self, action):
        obs = 0
        done = False
        if action[0] == COOPERATE and action[1] == DEFECT:
            reward = (0, 5)
        elif action[0] == DEFECT and action[1] == COOPERATE:
            reward = (5, 0)
        elif action[0] == COOPERATE and action[1] == COOPERATE:
            reward = (3, 3)
        elif action[0] == DEFECT and action[1] == DEFECT:
            reward = (1, 1)

        self.record_outcome = (self.iteration_number, action, reward)

        if self.iteration_number >= (self.m - 1):
            done = True

        self.iteration_number += 1

        return obs, reward, done, {}

    def render(self):
        if self.record_outcome == None:
            print('Start game.')
        else:
            iter, action, reward = self.record_outcome
            print('Iteration: ' + str(iter))
            print('Player 1 | action: ' +
                  WORD_FOR_ACTION[action[0]] + ' reward:' + str(reward[0]))
            print('Player 2 | action: ' +
                  WORD_FOR_ACTION[action[1]] + ' reward:' + str(reward[1]))
            print(' ')
