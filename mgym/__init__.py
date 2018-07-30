from gym.envs.registration import register
from mgym.core import MEnv

register(
    id='TicTacToe-v0',
    entry_point='mgym.envs:TicTacToeEnv',
)

register(
    id='RockPaperScissors-v0',
    entry_point='mgym.envs:RockPaperScissorsEnv',
)

register(
    id='RepeatedPrisonersDilemma-v0',
    entry_point='mgym.envs:RepeatedPrisonersDilemmaEnv',
)
