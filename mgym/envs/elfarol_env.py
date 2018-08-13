import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
import copy


class ElFarolEnv(mgym.MEnv):
    """
    El Farol N-person Game


    Example
    -------
    >>> import gym
    >>> import mgym
    >>> import random
    >>>
    >>> env = gym.make('ElFarol-v0')
    >>> obs = env.reset(N=10, total_iterations=100, threshold=0.6)
    >>> done = False
    >>> while True:
    ...     a = env.action_space.sample()
    ...     obs,r,done,info = env.step(a)
    ...     env.render()
    ...     if done:
    ...         break

 """

    def __init__(self):
        self.N = None  # Set in reset function
        self.nA = 2
        self.action_space = None
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(1,))
        self.state = None
        self.attendence_threshold = None
        self.WORD_FOR_ACTION = {0: 'STAY HOME',
                                1: 'GO TO BAR'}
        self.iteration = 0

    def reset(self,  N=10, total_iterations=100, threshold=0.6):
        """ Resets game """
        self.N = N
        self.action_space = spaces.Tuple(
            [spaces.Discrete(self.nA) for _ in range(self.N)])
        self.state = np.array([0.])
        self.iteration = 0
        self.total_iterations = total_iterations
        self.attendence_threshold = threshold
        return self.state

    def step(self, actions):
        """ steps environment with actionsself.

        Arguments
        ----------
            actions: joint actions for all players
        Returns
        -------
            returns tuple with
            self.state(observation): shared observation of the fraction of 
                people who went to bar
            rewards: tuple of rewards for each agent.
            done: boolean indicating if environment is done
            info: dict (empty for now)

        """
        self.iteration += 1
        if self.iteration >= self.total_iterations:
            done = True
        else:
            done = False
        self.state = np.array([sum(list(actions)) / self.N])
        crowded = (self.state[0] > 0.6)
        rewards = []
        for action in actions:
            if action == 1:
                if crowded:
                    reward = -1
                else:
                    reward = +1
            else:
                reward = 0
            rewards.append(reward)
        info = {}
        return self.state, rewards, done, info

    def render(self):
        print('\n Bar: {} Home: {}'.format(self.state[0], 1. - self.state[0]))
