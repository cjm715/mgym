from gym.envs.registration import register
from mgym.core import MEnv

register(
    id='TicTacToe-v0',
    entry_point='mgym.envs:TicTacToeEnv',
)

register(
    id='RPS-v0',
    entry_point='mgym.envs:RockPaperScissorsEnv',
)
