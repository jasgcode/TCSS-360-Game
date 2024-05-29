import random
import sys
import numpy as np
from src.model.Maze.Cells import Cells

sys.setrecursionlimit(8000)


class Maze:

    def __init__(self, width, height):
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height
        self.Cells = Cells()
        self.maze = None

    def create(self):
        maze = np.ones((self.height, self.width), dtype=float)
        # mid_height = self.height // 2
        # mid_width = self.width // 2
        randomVar = random.randrange(2, 25, 2)

        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:
                    maze[i, j] = 0
                if i == 0 or j == 0 or i == self.height - 1 or j == self.width - 1:
                    maze[i, j] = 0.5

        # maze1 = maze[0:mid_height, 0:mid_width].copy()
        # maze2 = maze[mid_height + 2:, 0:mid_width].copy()
        # maze3 = maze[0:mid_height, mid_width + 2:].copy()
        # maze4 = maze[mid_height + 2:, mid_width + 2:].copy()
        #
        # self.generate_sub_maze(maze1)
        # self.generate_sub_maze(maze2)
        # self.generate_sub_maze(maze3)
        # self.generate_sub_maze(maze4)
        #
        # maze[0:mid_height, 0:mid_width] = maze1
        # maze[mid_height + 2:, 0:mid_width] = maze2
        # maze[0:mid_height, mid_width + 2:] = maze3
        # maze[mid_height + 2:, mid_width + 2:] = maze4

        # version without border
        # maze1 = maze[0:mid_height, 0:mid_width].copy()
        # maze2 = maze[mid_height :, 0:mid_width].copy()
        # maze3 = maze[0:mid_height, mid_width:].copy()
        # maze4 = maze[mid_height :, mid_width :].copy()
        #
        # self.generate_sub_maze(maze1)
        # self.generate_sub_maze(maze2)
        # self.generate_sub_maze(maze3)
        # self.generate_sub_maze(maze4)
        #
        # maze[0:mid_height, 0:mid_width] = maze1
        # maze[mid_height:, 0:mid_width] = maze2
        # maze[0:mid_height, mid_width:] = maze3
        # maze[mid_height: , mid_width:] = maze4
        sx = random.choice(range(randomVar, self.width - 2, randomVar))
        sy = random.choice(range(randomVar, self.height - 2, randomVar))

        self.Cells.generator(sx, sy, maze)
        for i in range(self.height):
            for j in range(self.width):
                if maze[i, j] == 0.5:
                    maze[i, j] = 1

        maze[1, 2] = 1
        maze[self.height - 2, self.width - 3] = 1
        self.maze = maze

    def generate_sub_maze(self, sub_maze):
        if sub_maze.shape[1] <= 3 or sub_maze.shape[0] <= 3:
            return

        sx = random.randrange(2, sub_maze.shape[1] - 1, 2)
        sy = random.randrange(2, sub_maze.shape[0] - 1, 2)
        self.Cells.generator(sx, sy, sub_maze)

    def is_walkable(self, position):
        return not (self.width > position.x > 0 == self.maze[position.y, position.x] and
                    0 < position.y < self.height)
