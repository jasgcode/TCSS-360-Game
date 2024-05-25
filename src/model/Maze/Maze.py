import random
import numpy as np
from src.model.Maze.Cells import Cells


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
        randomVar = random.randrange(2, 25, 2)

        randomVar = random.randrange(2, 25, 2)

        randomVar = random.randrange(2,25,2)



        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:
                    maze[i, j] = 0
                if i == 0 or j == 0 or i == self.height - 1 or j == self.width - 1:
                    maze[i, j] = 0.5

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
        return maze


    def is_walkable(self, position):
        return (self.width > position.x >= 0 != self.maze[
            position.y, position.x] and 0 <= position.y < self.height)  # Check if the cell is not a wall
