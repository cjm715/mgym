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
    id='PrisonersDilemma-v0',
    entry_point='mgym.envs:PrisonersDilemmaEnv',
)

register(
    id='BattleOfTheSexes-v0',
    entry_point='mgym.envs:BattleOfTheSexesEnv',
)

register(
    id='StagHunt-v0',
    entry_point='mgym.envs:StagHuntEnv',
)

register(
    id='MatchingPennies-v0',
    entry_point='mgym.envs:MatchingPenniesEnv',
)

register(
    id='ElFarol-v0',
    entry_point='mgym.envs:ElFarolEnv',
)

register(
    id='Snake-v0',
    entry_point='mgym.envs:SnakeEnv',
)
