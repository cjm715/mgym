"""Traveling Checkers Environment."""
import mgym
from gym import spaces
import collections

MAX_NUM_AGENT_REQUEST = 10
output = collections.namedtuple('output', field_names=(
    'observation', 'reward', 'done', 'info'))

MOVEMENT = {0: (0, 0),
            1: (0, -1),
            2: (0, +1),
            3: (-1, 0),
            4: (+1, 0),
            }


class TravelingCheckersEnv(mgym.MEnv):
    """An environment of traveling checkers on a gridworld mimicing traffic.

    Original environnemt was introduced as a research challenge by the Santa Fe
    Institute's Complexity Challenge [CC]. The environment presented is
    slightly modified. The grid size is left arbitrary and the reward design
    was originally left open-ended.

    Overview: You have a M x M square checkerboard and there can be at most one
    checker on any given square at any time. Any number of checkers can be
    added to the environment at anytime. When a checker arrives on the
    left-most column it is randomly assigned to a destination square on the
    right-most column (anytime a checker arrives on the right-most column it is
    removed from the board). At each time step, a checker can either stay put
    or move to an adjacent square in any of the four cardinal directions as
    long as that adjacent square is open at the start of the time step (if more
    than one checker wants to move to the same square, one is randomly chosen
    to occupy the square and the others must stay put). Checkers must make
    their movement decisions based on a set of local rules (potentially unique
    to each checker) that only use information about the checker’s current
    position on the board, its destination, and whether squares in a local
    neighborhood are occupied. The local neighborhood consists of all squares
    that could be reached in R steps in the cardinal directions across adjacent
    checkers.

    update type :
        Synchronous
    individual agent observations :
        local Moore neighborhood with radius R plus waiting pool state
    individual agent actions :
        stay (0), south (1), north (2), east (3), and west (4)
    individual rewards :
        agent recieves a reward of -1 at each time step, +10 for reaching goal

    Args
    ----
    M : Grid side length
    N : Number of agents

    References
    ----------
    .. [CC] https://www.complexityexplorer.org/challenges/1-launch-of-the-complexity-challenges/submissions

    """

    def __init__(self, N=80, M=100):
        self.nA = 5
        self.S_neighborhood = 3**4
        self.N = N
        self.M
        super(TravelingCheckersEnv).__init__()

        ind_observation_space =

        self.observation_space = spaces.Tuple((
            spaces.Tuple((
                spaces.Discete(self.M),
                spaces.Discete(self.M),
                spaces.Discete(self.M),
                spaces.Discete(self.S_neighborhood)
            )) for _ in range(self.N)
        ))
        self.action_space = spaces.Tuple(
            (spaces.Discete(self.nA) for _ in range(self.N))
        )

        self.board = Board({})
        self.pool = Pool({i: Checker(i) for i in range(self.N)})

    def reset(self):
        """Reset environment and returns initial observations."""

        return observations

    def step(self, action_agents_dict):
        """Step environment with action and return observations, rewards, done,
        and info."""

        return observations, rewards, done, info

    def render(self):
        """Render environment."""
        pass


# class Checker(object):
#     """ A Checker lives off and on the board.
#
#     Arguments
#     ---------
#     onboard : boolean : states if checker is on or off board.
#     pos : 2 element list of integers and None if off board
#     des : 2 element list of integers and None if off board
#
#     Example
#     -------
#     >>> ch = Checker(False)
#     >>> ch
#     Checker(False,None,None)
#     >>> ch.add([1, 2],[3, 4])
#     >>> ch
#     Checker(True,[1, 2],[3, 4])
#     >>> ch.remove()
#     >>> ch
#     Checker(False,None,None)
#
#
#     """
#
#     def __init__(self, onboard, pos=None, des=None):
#         self._onboard = onboard
#         if self._onboard == True:
#             if (pos == None or des == None):
#                 raise Exception('Specify position and destination of checker.')
#
#         self._pos = pos
#         self._des = des
#
#     def remove(self):
#         """ Removes checker from board. """
#         if not self._onboard:
#             raise Except('Can not remove checker when off board')
#         self._pos = None
#         self._des = None
#         self._onboard = False
#
#     def get_state(self):
#         return (self._onboard, self._pos, self._des)
#
#     def add(self, pos=None, des=None):
#         if self._onboard:
#             raise Except('Can not add checker when already on board')
#
#         self._pos = pos
#         self._des = des
#         self._onboard = True
#
#     def move(self, action):
#         if self._onboard:
#             self._pos[0] = self._pos[0] + MOVEMENT[action][0]
#             self._pos[1] = self._pos[1] + MOVEMENT[action][1]
#         else:
#             raise Exception('Checker is off board.')
#
#     def __repr__(self):
#         return 'Checker({},{},{})'.format(self._onboard, self._pos, self._des)
#

class Checker(object):
    """ A Checker lives off and on the board.

    Arguments
    ---------
    pos : 2 element list of integers , default is None
    des : 2 element list of integers , default is None

    """

    def __init__(self, id, pos=None, des=None):
        self.id = id
        self.reset(pos, des)

    def proposed_pos(self, action):
        proposed_pos0 = self._pos[0] + MOVEMENT[action][0]
        proposed_pos1 = self._pos[1] + MOVEMENT[action][1]
        return [proposed_pos0, proposed_pos1]

    def move(self, action):
        self.pos = proposed_pos(self, action)

    def reset(self, pos=None, des=None):
        self._pos = pos
        self._des = des

    def __repr__(self):
        return 'Checker(pos = {}, des = {})'.format(self._pos, self._des)
