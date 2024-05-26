import unittest
from src.model.Maze.Maze import _Maze

class TestMaze(unittest.TestCase):
    def test_create_maze(self):
        width = 21
        height = 21
        maze = _Maze(height, width)
        maze.create()

        # Print the generated maze
        for row in maze.maze:
            for cell in row:
                if cell == 1:
                    print("  ", end="")
                elif cell == 0:
                    print("##", end="")
            print()

        # Check if the maze has the correct dimensions
        self.assertEqual(maze.maze.shape, (height, width))

        # Check if the maze has a walkable path from start to end
        start_pos = (3, 1 )
        end_pos = (height - 2, width - 3)
        self.assertEqual(maze.maze[start_pos[0], start_pos[1]], 1)
        self.assertEqual(maze.maze[end_pos[0], end_pos[1]], 1)

        # Check if the maze is surrounded by walls
        for i in range(height):
            self.assertEqual(maze.maze[i, 0], 0)
            self.assertEqual(maze.maze[i, width - 1], 0)
        for j in range(width):
            self.assertEqual(maze.maze[0, j], 0)
            self.assertEqual(maze.maze[height - 1, j], 0)

if __name__ == '__main__':
    unittest.main()