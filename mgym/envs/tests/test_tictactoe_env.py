from mgym.envs.tictactoe_env import TicTacToeEnv
import numpy as np
import random
import pytest


def test_that_tictactoe_run_without_error(env_name):
    env = gym.make('TicTacToe-v0')
    fullobs = env.reset()
    while True:
        print('Player O ') if fullobs[0] else print('Player X')
        a = random.choice(env.get_available_actions())
        fullobs, rewards, done, _ = env.step(a)
        env.render()
        if done:
            break

    assert True
