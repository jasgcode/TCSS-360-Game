import random


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
        self.grid = [[True] * width for _ in range(height)]
        self.generate_maze()

    def generate_maze(self):
        # Generate a simple maze grid
        self.grid = [
            [True, True, True, True, True],
            [True, False, False, False, True],
            [True, True, True, False, True],
            [True, False, True, False, True],
            [True, False, True, True, True]
        ]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def is_walkable(self, position):
        return 0 <= position.x < self.width and 0 <= position.y < self.height and self.grid[position.y][position.x]

class GameModel:
    def __init__(self):
        self.maze = None
        self.player = None
        self.score = 0
        self.timer = 0
        self.difficulty_level = None
        self.trivia_question_interval = 0
        self.trivia_question_timer = 0

    def initialize_game(self):
        self.maze = self.generate_maze()
        self.player = Player(Position(0, 0))
        self.score = 0
        self.timer = 0
        self.trivia_question_timer = 0

    def generate_maze(self):
        if self.difficulty_level == "Easy":
            width = 10
            height = 10
        elif self.difficulty_level == "Medium":
            width = 15
            height = 15
        else:  # "Hard"
            width = 20
            height = 20
        return Maze(width, height)

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
        new_position = self.player.position + direction
        if self.maze.is_walkable(new_position):
            self.player.move(direction)
            self.score += 1

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