import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym

ROCK = 0
PAPER = 1
SCISSORS = 2

WORD_FOR_ACTION = {0: 'ROCK',
                   1: 'PAPER',
                   2: 'SCISSORS'}


class RockPaperScissorsEnv(mgym.MEnv):
    '''
    Repeated Rock-Paper-Scissors
    '''

    def __init__(self):
        self.n = 2  # number of players
        self.nA = 3  # number of actions per player(rock, paper, or scissors)
        # There are no states! It is a single-shot game. To fit env clas we must
        # specify an observation space anyway. Thus we will say there is one state and always
        # one state.
        self.nS = 1
        self.record_outcome = None
        self.iteration = 0
        self.total_iterations = None
        # Joint action space across all players
        self.action_space = spaces.Tuple((
            spaces.Discrete(self.nA), spaces.Discrete(self.nA)))
        self.observation_space = spaces.Discrete(self.nS)

    def reset(self, total_iterations=100):
        self.record_outcome = None
        self.iteration = 0
        self.total_iterations = total_iterations
        return 0

    def step(self, action):
        obs = 0
        rewards = self._get_rewards(action)
        done = False
        if rewards[0] > rewards[1]:
            who_won = 0
        elif rewards[1] > rewards[0]:
            who_won = 1
        else:
            who_won = None
        self.record_outcome = (who_won, action)

        if self.iteration >= (self.total_iterations - 1):
            done = True

        self.iteration += 1
        return obs, rewards, done, {}

    def render(self):
        if self.record_outcome == None:
            print('Game has not started.')
        else:
            who_won, action = self.record_outcome
            print(' ')
            print('Player 1: ' + WORD_FOR_ACTION[action[0]])
            print('Player 2: ' + WORD_FOR_ACTION[action[1]])
            if who_won == None:
                print('Game is tied.')
            elif who_won == 0:
                print('Player 1 won!')
            elif who_won == 1:
                print('Player 2 won!')

    def _get_rewards(self, action):
        # Cases where player 1 wins
        if action[0] == ROCK and action[1] == SCISSORS:
            return (1, -1)
        if action[0] == SCISSORS and action[1] == PAPER:
            return (1, -1)
        if action[0] == PAPER and action[1] == ROCK:
            return (1, -1)

        # Cases where player 2 wins
        if action[1] == ROCK and action[0] == SCISSORS:
            return (-1, 1)
        if action[1] == SCISSORS and action[0] == PAPER:
            return (-1, 1)
        if action[1] == PAPER and action[0] == ROCK:
            return (-1, 1)

        # otherwise
        return (0, 0)
