import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
import copy


class RepeatedTwoPlayerGame(mgym.MEnv):

    def __init__(self, U, WORD_FOR_ACTION=None):
        # Utility matrix (list with shape (nA,nA) and tuple entries (reward1,reward2))
        self.U = U
        self.n = 2  # number of players
        # number of actions per player(rock, paper, or scissors)
        self.nA = len(self.U)
        assert len(self.U) == len(self.U[0])
        # This is a one-state MDP.
        self.nS = 1
        self.record_outcome = None
        self.iteration = 0
        self.total_iterations = None
        # Joint action space across all players
        self.action_space = spaces.Tuple((
            spaces.Discrete(self.nA), spaces.Discrete(self.nA)))
        self.observation_space = spaces.Discrete(self.nS)
        if WORD_FOR_ACTION == None:
            self.WORD_FOR_ACTION = {
                i: 'Action ' + str(i) for i in range(self.nA)}
        else:
            self.WORD_FOR_ACTION = WORD_FOR_ACTION

    def reset(self, total_iterations=100):
        self.record_outcome = None
        self.iteration = 0
        self.total_iterations = total_iterations
        return 0

    def step(self, action):
        obs = 0
        rewards = self._get_rewards(action)
        done = False
        self.record_outcome = (self.iteration, action, rewards)

        if self.iteration >= (self.total_iterations - 1):
            done = True

        self.iteration += 1
        return obs, rewards, done, {}

    def render(self):
        if self.record_outcome == None:
            print('Game has not started.')
        else:
            iter, action, rewards = self.record_outcome
            if rewards[0] > rewards[1]:
                who_won = 0
            elif rewards[1] > rewards[0]:
                who_won = 1
            else:
                who_won = None
            print(' ')
            print('Iteration: ' + str(iter))
            print('Player 1 | action: ' +
                  self.WORD_FOR_ACTION[action[0]] + ' reward:' + str(rewards[0]))
            print('Player 2 | action: ' +
                  self.WORD_FOR_ACTION[action[1]] + ' reward:' + str(rewards[1]))
            if who_won == None:
                print('Game is tied.')
            elif who_won == 0:
                print('Player 1 won!')
            elif who_won == 1:
                print('Player 2 won!')

    def _get_rewards(self, action):
        return self.U[action[0]][action[1]]

    def show_utility(self):
        print(self.U)
