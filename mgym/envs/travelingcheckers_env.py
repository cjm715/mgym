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

        self.board = Board()
        self.pool = Pool({i: Checker(i) for i in range(self.N)})

    def reset(self):
        """Reset environment and returns initial observations."""

        return observations

    def step(self, action_agents_dict):
        """Step environment with action and return observations, rewards, done, and info."""

        return observations, rewards, done, info

    def render(self):
        """Render environment."""
        pass


class Board(object):
    """ Board container object

    Arguments
    ---------
        M : int : size of board
        checkers : dict (default = {}): dictionary of checkers with key as id
        and value as Checker object.

    """

    def __init__(self, M, checkers=None):
        self.M = M
        if checkers == None:
            checkers = {}
        self.checkers = checkers

    def add(self, new_checkers):
        if isinstance(new_checkers, Checker):
            new_checkers_list = [new_checkers]
        else:
            new_checkers_list = new_checkers
        """ new_checkers is a dictionary of Checkers to be added to
        self.checkers """

        new_checkers_dict = {ch.id: ch for ch in new_checkers_list}
        self.checkers.update(new_checkers_dict)

    def pop(self, checker_id_list):
        return_dict = {}
        for id in checker_id_list:
            return_dict[id] = self.checkers.pop(id)
        return return_dict

    def get_board(self):
        board = [[None for _ in range(self.M)] for _ in range(self.M)]
        for i, ch in self.checkers.items():
            board[ch.pos[0]][ch.pos[1]] = i
        return board

    def __repr__(self):
        return 'Board({})'.format(self.M)

    def __str__(self):
        board = self.get_board()
        board_str = ''
        for i in range(self.M):
            for j in range(self.M):
                board_str += '|'
                if board[i][j] == None:
                    board_str += ' '
                else:
                    board_str += str(board[i][j])
            board_str += '|\n'
        return board_str


class Pool(object):
    """ Waiting pool for checkers."""

    def __init__(self, checkers=None):
        if checkers == None:
            checkers = {}
        self.checkers = checkers

    def add(self, new_checkers):
        """ new_checkers is a dictionary of Checkers to be added to
        self.checkers """

        # Accepts a single checker as input but converts to list with single element
        if isinstance(new_checkers, Checker):
            new_checkers_list = [new_checkers]
        else:
            new_checkers_list = new_checkers

        for ch in new_checkers_list:
            ch.reset()

        new_checkers_dict = {ch.id: ch for ch in new_checkers_list}
        self.checkers.update(new_checkers_dict)

    def pop_random_item(self):
        random_key = random.choice(self.checkers.keys())
        random_value = self.checkers.pop(random_key)
        return random_key, random_value

    def __repr__(self):
        return 'Pool({})'.format(self.checkers.__repr__())


class Checker(object):
    """ A Checker lives off and on the board.

    Arguments
    ---------
    id: int to specify checker's unique id number.
    pos : 2 element list of integers , default is None
    des : 2 element list of integers , default is None

    """

    def __init__(self, id, pos=None, des=None):
        self.id = id
        self.reset(pos, des)

    def proposed_pos(self, action):
        proposed_pos0 = self.pos[0] + MOVEMENT[action][0]
        proposed_pos1 = self.pos[1] + MOVEMENT[action][1]
        return [proposed_pos0, proposed_pos1]

    def move(self, action):
        self.pos = proposed_pos(self, action)

    def reset(self, pos=None, des=None):
        self.pos = pos
        self._des = des

    def __repr__(self):
        return 'Checker(id = {}, pos = {}, des = {})'.format(self.id, self.pos, self._des)
