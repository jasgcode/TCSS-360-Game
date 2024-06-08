import random
import sys
import numpy as np
from src.model.Maze.Cells import Cells

sys.setrecursionlimit(8000)


class Maze:
    def __init__(self, width, height):
        """
        Initialize the maze with specified width and height.
        """
        self.end_pos = None
        self.start_pos = None
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height
        self.Cells = Cells()
        self.maze = None
        self.maze1start = False

    def create(self):
        """
        Create the maze using a recursive backtracking algorithm.
        """
        maze = np.ones((self.height, self.width), dtype=float)
        # mid_height = self.height // 2
        # mid_width = self.width // 2
        randomVar = random.randrange(2, 18, 2)

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

        self.start_pos = (1, 2)  # Store the starting position as a tuple
        self.end_pos = (self.height - 3, self.width - 4)  # Store the ending position as a tuple

        maze[self.start_pos[0], self.start_pos[1]] = 0.6
        maze[self.end_pos[0], self.end_pos[1]] = 0.75
        self.maze = maze

    # def generate_sub_maze(self, sub_maze):
    #     if sub_maze.shape[1] <= 3 or sub_maze.shape[0] <= 3:
    #         return
    #
    #     sx = random.randrange(2, sub_maze.shape[1] - 1, 2)
    #     sy = random.randrange(2, sub_maze.shape[0] - 1, 2)
    #     self.Cells.generator(sx, sy, sub_maze)

    def is_walkable(self, position):
        """
        Check if the position is walkable (not a wall) in the maze.
        """
        return not (self.width > position.x > 0 == self.maze[position.y, position.x] and
                    0 < position.y < self.height)
