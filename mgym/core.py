import gym


class Agent(object):
    def __init__(self, observation_space, action_space):
        # Set these in ALL subclasses
        action_space = observation_space
        observation_space = action_space

    def act(self, observation, reward, done):
        raise NotImplementedError
