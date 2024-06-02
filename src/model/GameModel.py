import os
import pickle

from src.model.Maze.Maze import Maze
from src.model.Entity.Player import Player
from src.model.Entity.Mob import Mob
from src.model.Entity.Entity import Position
from src.model.TriviaManager.TriviaManager import TriviaManager

import random


class GameModel:
    def __init__(self):
        self.maze = None
        self.maze1 = None
        self.maze2 = None
        self.maze3 = None
        self.maze4 = None
        self.player = None
        self.num_mobs = None
        self.trivia_manager = None
        self.mobs = []
        self.mobs_positions = []
        self.mob_hunt = None
        self.score = 0
        self.timer = 0
        self.difficulty_level = "Easy"
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
        self.mobs = []
        self.mobs_positions = []
        for _ in range(self.num_mobs):
            mob_position = self.mob_spawn(self.maze)
            self.mobs.append(Mob(mob_position))
            self.mobs_positions.append(mob_position)
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
        self.trivia_manager = TriviaManager(difficulty_level.lower())
        if difficulty_level == "Easy":
            self.trivia_question_interval = 20
            self.num_mobs = 5
        elif difficulty_level == "Medium":
            self.trivia_question_interval = 15
            self.num_mobs = 10
        else:  # "Hard"
            self.trivia_question_interval = 10
            self.num_mobs = 25

    @staticmethod
    def get_position(x, y):
        return Position(x, y)

    def update_game_state(self):
        self.timer += 1
        self.trivia_question_timer += 1

    def mob_spawn(self, maze):
        while True:
            x = random.randrange(1, maze.width - 1)
            y = random.randrange(1, maze.height - 1)
            position = Position(x, y)
            if position.is_valid(maze) and position.is_walkable(maze):
                return position

    def check_mob_encounter(self):
        for i, mob_position in enumerate(self.mobs_positions):
            if self.player.position.x == mob_position.x and self.player.position.y == mob_position.y:
                if self.mobs[i].fight:
                    return i
        return None

    def move_player(self, direction):
        self.player.move(direction, self.maze)

    def remove_mob(self, mob_index):
        self.mobs.pop(mob_index)
        self.mobs_positions.pop(mob_index)

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

    def get_trivia_question(self):
        if self.trivia_manager:
            return self.trivia_manager.get_trivia_question()
        else:
            return None

    def close_trivia_manager(self):
        if self.trivia_manager:
            self.trivia_manager.close_database()

    def generate_save_file_name(self):
        save_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Generate the file name based on the number of existing save files
        save_files = [file for file in os.listdir(save_directory) if file.startswith('save')]
        save_number = len(save_files) + 1
        file_name = f'save{save_number}.pkl'

        return file_name

    def save_game_state(self, file_name):
        save_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
        file_path = os.path.join(save_directory, file_name)
        game_state = {
            'maze': self.maze,
            'player': self.player,
            'mobs': self.mobs,
            'score': self.score,
            'difficulty_level': self.difficulty_level,
            # Add other attributes you want to save
        }
        with open(file_path, 'wb') as file:
            pickle.dump(game_state, file)

    def load_game_state(self, file_name):
        save_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
        file_path = os.path.join(save_directory, file_name)
        with open(file_path, 'rb') as file:
            game_state = pickle.load(file)
        self.maze = game_state['maze']
        self.player = game_state['player']
        self.mobs = game_state['mobs']
        self.score = game_state['score']
        self.difficulty_level = game_state['difficulty_level']
        # Assign other loaded attributes to the game model
