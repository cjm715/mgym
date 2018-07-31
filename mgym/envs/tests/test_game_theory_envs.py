import mgym
import gym
import numpy as np
import random
import pytest


@pytest.mark.parametrize("env_name", [
    'RockPaperScissors-v0',
    'PrisonersDilemma-v0',
    'BattleOfTheSexes-v0',
    'StagHunt-v0',
    'MatchingPennies-v0',
])
def test_that_all_2player_game_theory_environments_run_without_error(env_name):

    env = gym.make(env_name)
    obs = env.reset(6)
    while True:
        a = env.action_space.sample()
        _, r, done, _ = env.step(a)
        env.render()
        print(r)
        if done:
            break

    assert True
