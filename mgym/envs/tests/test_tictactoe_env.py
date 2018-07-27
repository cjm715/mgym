from mgym.envs.tictactoe_env import TicTacToeEnv
import numpy as np


def test_tictactoe_env_reset():
    env = TicTacToeEnv()
    assert np.allclose(np.zeros(env.shape), env.reset())
