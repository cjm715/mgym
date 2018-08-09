"""Traveling Checkers Environment."""
import mgym


class TravelingCheckersEnv(mgym.MEnv):
    """An environment of traveling checkers on a gridworld mimicing traffic.

    Original environnemt was introduced as a research challenge by the Santa Fe
    Institute's Complexity Challenge [CC]. The environment presented is
    slightly modified. The grid size is left arbitrary and the reward design
    was originally left open-ended.

    Overview: You have a M x M square checkerboard and there can be at most one
    checker on any given square at any time. At each time step one or more
    checkers randomly appear on squares in the left-most column of the board.
    When a checker arrives on the left-most column it is randomly assigned to a
    destination square on the right-most column (anytime a checker arrives on
    the right-most column it is removed from the board). At each time step, a
    checker can either stay put or move to an adjacent square in any of the
    four cardinal directions as long as that adjacent square is open at the
    start of the time step (if more than one checker wants to move to the same
    square, one is randomly chosen to occupy the square and the others must
    stay put). Checkers must make their movement decisions based on a set of
    local rules (potentially unique to each checker) that only use information
    about the checker’s current position on the board, its destination, and
    whether squares in a local neighborhood are occupied. The local
    neighborhood consists of all squares that could be reached in R steps in
    the cardinal directions across adjacent checkers.

    update type :
        Synchronous
    individual agent observations :
        local Moore neighborhood with radius R
    individual agent actions :
        stay (0), south (1), north (2), east (3), and west (4)
    individual rewards :
        agent recieves a reward of -1 at each time step, +10 for reaching goal

    Args
    ----
    M : Grid side length

    Attributes
    ----------
    observation_space : Joint tuple space of discrete spaces for each agent.
    action_space :  Joint tuple space of discrete spaces for each agent.

    References
    ----------
    .. [CC] https://www.complexityexplorer.org/challenges/1-launch-of-the-complexity-challenges/submissions


    """

    def __init__(self):
        pass

    def reset(self):
        """Reset environment."""
        pass

    def step(self, action):
        """Step environment with action."""
        pass

    def render(self, action):
        """Render environment."""
        pass
