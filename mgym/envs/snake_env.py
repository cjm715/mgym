"""Snake environment"""
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import mgym
import copy
import pyglet
from collections import deque
import random

GRID_HEIGHT = 30
GRID_WIDTH = 30
GRID_SIZE = 15
MARGIN = 1
APPLE_ID = 1
WALL_ID = 2
NUM_APPLES = 2


class SnakeEnv(mgym.MEnv):
    """ Multi-agent version of classic Nokia snake game.

    This environment is proposed in the OpenAI's request-for-research page [RR]. This request is inspired by
    slither.io [SL].

    References
    ---------
    .. [RR] https://blog.openai.com/requests-for-research-2/
    .. [SL] http://slither.io/

    """

    def __init__(self):
        self.N = None  # set in reset function

    def reset(self, N):
        self.done = False
        self.N = N
        self.nA = 4
        self.observation_space = spaces.Box(low=0, high=self.N + 2, shape=(
            GRID_HEIGHT, GRID_WIDTH), dtype=np.uint8)
        self.action_space = spaces.Tuple(
            [spaces.Discrete(self.nA) for _ in range(self.N)])
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))
        self.apples = []
        self.snakes = []
        self.walls = []
        self.create_boarder()

        for i in range(N):
            snake_id = 3 + i
            location = self._get_empty_location()
            self.snakes.append(Snake(*location, snake_id))

        for i in range(NUM_APPLES):
            location = self._get_empty_location()
            self.apples.append(Apple(*location))

        self.update_grid()

    def create_boarder(self):
        self.walls = []

        # south wall
        for i in range(GRID_WIDTH):
            self.walls.append(Wall(i, 0))

        # north wall
        for i in range(GRID_WIDTH):
            self.walls.append(Wall(i, GRID_HEIGHT - 1))

        # west wall
        for i in range(1, GRID_HEIGHT - 1):
            self.walls.append(Wall(0, i))

        # east wall
        for i in range(1, GRID_HEIGHT - 1):
            self.walls.append(Wall(GRID_HEIGHT - 1, i))

    def step(self, action):
        for i, snake in enumerate(self.snakes):
            snake.update_head(action[i])

        num_apples_eaten = 0
        for snake in self._alive_snakes():
            i = 0
            on_apple = False
            while i < len(self.apples):
                apple = self.apples[i]
                on_apple = (snake.x, snake.y) == (apple.x, apple.y)
                if on_apple:
                    del self.apples[i]
                    num_apples_eaten += 1
                    break
                i += 1

            snake.update_tail(action, on_apple)

        for _ in range(num_apples_eaten):
            location = self._get_empty_location()
            self.apples.append(Apple(*location))

        self.remove_dead_snakes()

        if not self._alive_snakes():
            self.done = True
            print('\n')
            print('*******************')
            print('**** GAME OVER ****')
            print('******************* \n')

        self.update_grid()

        rewards = [len(snake.tail) for snake in self.snakes]

        return self.grid, rewards, self.done, {}

    def remove_dead_snakes(self):
        restricted_sites = set()

        for snake in self._alive_snakes():
            for tail_elem in list(snake.tail)[1:]:
                restricted_sites.add(tail_elem)

        for wall in self.walls:
            restricted_sites.add((wall.x, wall.y))

        for snake in self._alive_snakes():
            if (snake.x, snake.y) in restricted_sites:
                print('SNAKE {} DIED!'.format(snake.id - 2))
                snake.alive = False

    def render(self):
        for row in range(0, GRID_HEIGHT):
            for col in range(0, GRID_WIDTH):
                if self.grid[row, col] == APPLE_ID:
                    color = 'green'
                    self._draw_square(row, col, color)
                elif self.grid[row, col] == WALL_ID:
                    color = 'blue'
                    self._draw_square(row, col, color)
                elif self.grid[row, col] >= 3:
                    color = int((self.grid[row, col] - 3) /
                                self.N * (255 - MIN_COLOR) + MIN_COLOR)
                    self._draw_square(row, col, color)

    def update_grid(self):
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))
        for snake in self._alive_snakes():
            for tail_piece in snake.tail:
                self.grid[tail_piece[0], tail_piece[1]] = snake.id
        for apple in self.apples:
            self.grid[apple.x, apple.y] = apple.id
        for wall in self.walls:
            self.grid[wall.x, wall.y] = wall.id

    def _alive_snakes(self):
        return [snake for snake in self.snakes if snake.alive]

    def _get_empty_location(self):
        potential_sites = {(row, col) for row in range(0, GRID_HEIGHT)
                           for col in range(0, GRID_WIDTH)}
        restricted_sites = set()

        for snake in self._alive_snakes():
            for tail_elem in snake.tail:
                restricted_sites.add(tail_elem)

        for wall in self.walls:
            restricted_sites.add((wall.x, wall.y))

        for apple in self.apples:
            restricted_sites.add((apple.x, apple.y))

        avaliable_sites = potential_sites - restricted_sites
        if avaliable_sites:
            return random.choice(list(avaliable_sites - restricted_sites))
        else:
            raise Exception('No available sites')

    def _draw_square(self, row, col, color):

        if isinstance(color, int):
            RGB = (color, color, color)
        elif isinstance(color, str):
            if color == 'red':
                RGB = (255, 0, 0)
            elif color == 'green':
                RGB = (0, 255, 0)
            elif color == 'blue':
                RGB = (0, 0, 255)

        square_coords = (row * GRID_SIZE + MARGIN, col * GRID_SIZE + MARGIN,
                         row * GRID_SIZE + MARGIN, col * GRID_SIZE + GRID_SIZE - MARGIN,
                         row * GRID_SIZE + GRID_SIZE - MARGIN, col * GRID_SIZE + MARGIN,
                         row * GRID_SIZE + GRID_SIZE - MARGIN, col * GRID_SIZE + GRID_SIZE - MARGIN)
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                     [0, 1, 2, 1, 2, 3],
                                     ('v2i', square_coords),
                                     ('c3B', (*RGB, *RGB, *RGB, *RGB)))


class Apple(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = APPLE_ID


class Wall(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = WALL_ID


SPEED = {0: (0, -1),
         1: (0, 1),
         2: (-1, 0),
         3: (1, 0)}

OPPOSITE_DIRECTION = {0: 1,
                      1: 0,
                      2: 3,
                      3: 2}


class Snake(object):
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.direction = 2
        self.xspeed = SPEED[self.direction][0]
        self.yspeed = SPEED[self.direction][1]
        self.id = id
        self.tail = deque()
        self.tail.appendleft((self.x, self.y))
        self.alive = True
        self.freeapples = 40

    def update_head(self, action):
        if self.alive:
            if action != OPPOSITE_DIRECTION[self.direction]:
                self.direction = action

            self.xspeed = SPEED[self.direction][0]
            self.yspeed = SPEED[self.direction][1]

            self.x = (self.x + self.xspeed) % GRID_WIDTH
            self.y = (self.y + self.yspeed) % GRID_HEIGHT

    def update_tail(self, action, on_apple):

        if self.alive:
            if not (on_apple or self.freeapples > 0):
                self.tail.pop()
            self.tail.appendleft((self.x, self.y))

        self.freeapples -= 1


MIN_COLOR = 50


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(GRID_HEIGHT * GRID_SIZE, GRID_WIDTH * GRID_SIZE)
        self.env = SnakeEnv()
        pyglet.clock.schedule_interval(self.update, 1.0 / 8.0)
        self.action = [2, 2]
        self.pause = False

    def on_draw(self):
        self.clear()
        self.env.render()

    def update(self, dt):
        if not self.pause:
            # self.action = self.env.action_space.sample()
            s, r, d, _ = self.env.step(self.action)
            if self.env.done:
                self.close()

    def on_key_press(self, symbol, mod):

        if symbol == pyglet.window.key.S:
            self.action[0] = 0
        if symbol == pyglet.window.key.W:
            self.action[0] = 1
        if symbol == pyglet.window.key.A:
            self.action[0] = 2
        if symbol == pyglet.window.key.D:
            self.action[0] = 3

        if symbol == pyglet.window.key.DOWN:
            self.action[1] = 0
        if symbol == pyglet.window.key.UP:
            self.action[1] = 1
        if symbol == pyglet.window.key.LEFT:
            self.action[1] = 2
        if symbol == pyglet.window.key.RIGHT:
            self.action[1] = 3

        if symbol == pyglet.window.key.SPACE:
            self.pause = not self.pause


if __name__ == "__main__":
    num_snakes = 2
    wind = Window()
    wind.env.reset(num_snakes)
    pyglet.app.run()
