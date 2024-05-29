from src.model.Maze.Maze import Maze
from src.model.Entity.Player import Player
from src.model.Entity.Mob import Mob
from src.model.Entity.Entity import Position


class GameModel:
    def __init__(self):
        self.maze = None
        self.maze1 = None
        self.maze2 = None
        self.maze3 = None
        self.maze4 = None
        self.player = None
        self.mob = None
        self.mob_hunt = None
        self.score = 0
        self.timer = 0
        self.difficulty_level = None
        self.trivia_question_interval = 0
        self.trivia_question_timer = 0
        self.cell_size = 0

    def initialize_game(self, width, height, cell_size):
        self.maze1 = self.generate_maze(width, height)
        self.maze2 = self.generate_maze(width, height)
        self.maze3 = self.generate_maze(width, height)
        self.maze4 = self.generate_maze(width, height)
        self.maze = self.maze1
        self.player = Player(Position(2, 1))  # Starting position of the player
        self.mob = Mob(Position(width//2 - 2, 2))
        self.score = 0
        self.timer = 0
        self.trivia_question_timer = 0
        self.cell_size = cell_size

    @staticmethod
    def generate_maze(width, height):
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
            self.mob_hunt = True

    @staticmethod
    def get_position(x, y):
        return Position(x, y)

    def update_game_state(self):
        self.timer += 1
        self.trivia_question_timer += 1

    def move_player(self, direction):
        self.player.move(direction, self.maze)

    def move_enemy(self, maze, position):
        if self.mob_hunt is True:
            self.mob.find_path_to_player(maze, position)
            self.mob.move_along_path(self.mob, maze)

    def is_game_over(self):
        return self.player.position == Position(self.maze.height - 2, self.maze.width - 3)

    def should_ask_trivia_question(self):
        return self.trivia_question_timer >= self.trivia_question_interval

    def answer_trivia_question_correctly(self):
        self.score += 10
        self.trivia_question_timer = 0

    def answer_trivia_question_incorrectly(self):
        self.score -= 5
        self.trivia_question_timer = 0
