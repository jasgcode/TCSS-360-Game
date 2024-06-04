import os
import pickle

from src.model.Maze.Maze import Maze
from src.model.Entity.Player import Player
from src.model.Entity.Mob import Mob
from src.model.Entity.Entity import Position
from src.model.TriviaManager.TriviaManager import TriviaManager
from src.model.sound.SoundManager import SoundManager

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
        self.current_filename = None
        self.sound_manager = SoundManager()
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

        if self.current_filename is not None:
            for pos in self.mobs_positions:
                self.mobs.append(Mob(pos))
        else:
            # If starting a new game, generate new mob positions
            self.mobs_positions = []
            for _ in range(self.num_mobs):
                mob_position = self.mob_spawn(self.maze)
                self.mobs.append(Mob(mob_position))
                self.mobs_positions.append(mob_position)

        print("Initialized mobs:", self.mobs)
        print("Initialized mobs_positions:", self.mobs_positions)

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
            self.cell_size = 28
        elif difficulty_level == "Medium":
            self.trivia_question_interval = 15
            self.num_mobs = 10
            self.cell_size = 25
        else:  # "Hard"
            self.trivia_question_interval = 10
            self.num_mobs = 25
            self.cell_size = 19

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

    def return_button_sound(self, event):
        self.sound_manager.play_button_sound(event)

    def get_cell_size(self):
        return self.cell_size
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

    def get_save_files(self):
        save_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        # Generate the file name based on the number of existing save files
        save_files = [file for file in os.listdir(save_directory) if file.startswith('save')]
        return save_files

    def save_game_state(self, file_name):
        if file_name is None:
            file_name = self.generate_save_file_name()
        save_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
        file_path = os.path.join(save_directory, file_name)

        mob_data = [{'path': mob.path, 'fight': mob.fight} for mob in self.mobs]

        game_state = {
            'maze1': self.maze1,
            'maze2': self.maze2,
            'maze3': self.maze3,
            'maze4': self.maze4,
            'maze': self.maze,
            'player': self.player,
            'mobs': self.mobs,
            'mobs_positions': self.mobs_positions,
            'score': self.score,
            'difficulty_level': self.difficulty_level,
            'num_mobs': self.num_mobs,
            'mob_data': mob_data,  # Include mob_data in the game state
            'cell_size': self.cell_size,
        }

        with open(file_path, 'wb') as file:
            pickle.dump(game_state, file)

        self.current_filename = file_name

    def load_game_state(self, file_name):
        save_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
        file_path = os.path.join(save_directory, file_name)
        self.current_filename = file_name
        with open(file_path, 'rb') as file:
            game_state = pickle.load(file)
            self.maze1 = game_state['maze1']
            self.maze2 = game_state['maze2']
            self.maze3 = game_state['maze3']
            self.maze4 = game_state['maze4']
            self.maze = game_state['maze']
            self.player = game_state['player']
            self.mobs_positions = game_state['mobs_positions']
            self.mobs = [Mob(pos) for pos in self.mobs_positions]
            self.num_mobs = game_state['num_mobs']
            self.score = game_state['score']
            self.difficulty_level = game_state['difficulty_level']
            self.cell_size = game_state['cell_size']

            # Load additional attributes for each mob
            for i, mob_data in enumerate(game_state.get('mob_data', [])):
                self.mobs[i].path = mob_data['path']
                self.mobs[i].fight = mob_data['fight']

            print("Loaded mobs_positions:", self.mobs_positions)
            print("Loaded num_mobs:", self.num_mobs)

            # Initialize the TriviaManager based on the loaded difficulty level
            self.set_difficulty_level(self.difficulty_level)