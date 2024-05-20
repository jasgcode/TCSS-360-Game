import random
import numpy as np

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)


class Player:
    def __init__(self, position):
        self.position = position

    def move(self, direction):
        self.position += direction


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = None
        self.generate_maze(width, height)

    def generate_maze(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[True] * width for _ in range(height)]

        def carve_maze(x, y):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2

                if 0 <= nx < width and 0 <= ny < height and self.grid[ny][nx]:
                    self.grid[y + dy][x + dx] = False
                    self.grid[ny][nx] = False
                    carve_maze(nx, ny)

        # Start carving the maze from a random cell
        start_x = random.randint(0, (width - 1) // 2) * 2 + 1
        start_y = random.randint(0, (height - 1) // 2) * 2 + 1
        self.grid[start_y][start_x] = False
        carve_maze(start_x, start_y)
    def is_walkable(self, position):
        return 0 <= position.x < self.width and 0 <= position.y < self.height and self.grid[position.y][position.x]

import random
import numpy as np
from src.model.Maze.Maze import Maze
from src.model.Player.Player import Player, Position

class GameModel:
    def __init__(self):
        self.maze = None
        self.player = None
        self.score = 0
        self.timer = 0
        self.difficulty_level = None
        self.trivia_question_interval = 0
        self.trivia_question_timer = 0

    def initialize_game(self, width, height, cell_size):
        self.maze = self.generate_maze(width, height)
        self.player = Player(Position(0, 0))  # Starting position of the player
        self.score = 0
        self.timer = 0
        self.trivia_question_timer = 0

    def generate_maze(self, width, height):
        maze = Maze(width, height)
        maze.create()
        return maze

    def set_difficulty_level(self, difficulty_level):
        self.difficulty_level = difficulty_level
        if difficulty_level == "Easy":
            self.trivia_question_interval = 20
        elif difficulty_level == "Medium":
            self.trivia_question_interval = 15
        else:  # "Hard"
            self.trivia_question_interval = 10

    def update_game_state(self):
        self.timer += 1
        self.trivia_question_timer += 1

    def move_player(self, direction):
        new_position = Position(self.player.position.x + direction.x, self.player.position.y + direction.y)
        if new_position.is_valid(self.maze) and new_position.is_walkable(self.maze):
            self.player.move(direction, self.maze)

    def is_game_over(self):
        return self.player.position.x == self.maze.width - 2 and self.player.position.y == self.maze.height - 2

    def should_ask_trivia_question(self):
        return self.trivia_question_timer >= self.trivia_question_interval

    def answer_trivia_question_correctly(self):
        self.score += 10
        self.trivia_question_timer = 0

    def answer_trivia_question_incorrectly(self):
        self.score -= 5
        self.trivia_question_timer = 0

    def set_difficulty_level(self, difficulty_level):
        self.difficulty_level = difficulty_level
        if difficulty_level == "Easy":
            self.trivia_question_interval = 20
        elif difficulty_level == "Medium":
            self.trivia_question_interval = 15
        else:  # "Hard"
            self.trivia_question_interval = 10

    def update_game_state(self):
        self.timer += 1
        self.trivia_question_timer += 1

    def is_game_over(self):
        return self.player.position == Position(self.maze.width - 1, self.maze.height - 1)

    def should_ask_trivia_question(self):
        return self.trivia_question_timer >= self.trivia_question_interval

    def answer_trivia_question_correctly(self):
        self.score += 10
        self.trivia_question_timer = 0

    def answer_trivia_question_incorrectly(self):
        self.score -= 5
        self.trivia_question_timer = 0
