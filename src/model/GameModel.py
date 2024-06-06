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
        self.mobs1 = []
        self.mobs2 = []
        self.mobs3 = []
        self.mobs4 = []
        self.mobs_positions =[]
        self.mobs_positions1 = []
        self.mobs_positions2 = []
        self.mobs_positions3 = []
        self.mobs_positions4 = []
        self.visited_mazes = []
        self.mazes_to_visit = []
        self.mob_hunt = None
        self.lives = 5
        self.score = 0
        self.timer = 0
        self.current_filename = None
        self.sound_manager = SoundManager()
        self.difficulty_level = "Easy"
        self.trivia_question_interval = 0
        self.trivia_question_timer = 0
        self.cell_size = 0
        self.current_maze_index = 0

    def initialize_game(self, width, height, cell_size):
        self.maze1 = self.generate_maze(width, height)
        self.maze2 = self.generate_maze(width, height)
        self.maze3 = self.generate_maze(width, height)
        self.maze4 = self.generate_maze(width, height)
        self.maze1.maze1start = True
        self.mazes_to_visit = [self.maze4, self.maze3, self.maze2]
        self.maze = self.maze1
        self.player = Player(Position(2, 1))  # Starting position of the player
        self.mobs = []

        if self.current_filename is not None:
            self.mobs1 = [Mob(pos) for pos in self.mobs_positions1]
            self.mobs2 = [Mob(pos) for pos in self.mobs_positions2]
            self.mobs3 = [Mob(pos) for pos in self.mobs_positions3]
            self.mobs4 = [Mob(pos) for pos in self.mobs_positions4]
        else:
            # If starting a new game, generate new mob positions for each maze
            self.mobs_positions1 = [self.mob_spawn(self.maze1) for _ in range(self.num_mobs)]
            self.mobs_positions2 = [self.mob_spawn(self.maze2) for _ in range(self.num_mobs)]
            self.mobs_positions3 = [self.mob_spawn(self.maze3) for _ in range(self.num_mobs)]
            self.mobs_positions4 = [self.mob_spawn(self.maze4) for _ in range(self.num_mobs)]
            self.mobs1 = [Mob(pos) for pos in self.mobs_positions1]
            self.mobs2 = [Mob(pos) for pos in self.mobs_positions2]
            self.mobs3 = [Mob(pos) for pos in self.mobs_positions3]
            self.mobs4 = [Mob(pos) for pos in self.mobs_positions4]

        self.mobs = self.mobs1  # Set the initial mobs to mobs1
        self.mobs_positions = self.mobs_positions1

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
            self.lives = 5
        elif difficulty_level == "Medium":
            self.trivia_question_interval = 15
            self.num_mobs = 10
            self.cell_size = 25
            self.lives = 3
        else:  # "Hard"
            self.trivia_question_interval = 10
            self.num_mobs = 25
            self.cell_size = 19
            self.lives = 1

    @staticmethod
    def get_position(x, y):
        return Position(x, y)

    def update_game_state(self):
        self.timer += 1
        self.trivia_question_timer += 1

    def switch_to_next_maze(self):
        self.current_maze_index += 1
        if self.mazes_to_visit:
            self.visited_mazes.append(self.maze)
            self.maze = self.mazes_to_visit.pop()
            self.player = Player(Position(2, 1))

        if self.maze == self.maze4:
            self.mobs = self.mobs4
            self.mobs_positions = self.mobs_positions4
        elif self.maze == self.maze3:
            self.mobs = self.mobs3
            self.mobs_positions = self.mobs_positions3
        elif self.maze == self.maze2:
            self.mobs = self.mobs2
            self.mobs_positions = self.mobs_positions2

    def switch_to_previous_maze(self):
        self.current_maze_index -= 1
        if self.visited_mazes:
            self.mazes_to_visit.append(self.maze)
            self.maze = self.visited_mazes.pop()
            end_y, end_x = self.maze.end_pos
            self.player.position = Position(end_x,
                                            end_y)  # Set the player's position to the end_pos of the previous maze
        if self.maze == self.maze1:
            self.mobs = self.mobs1
            self.mobs_positions = self.mobs_positions1
        elif self.maze == self.maze2:
            self.mobs = self.mobs2
            self.mobs_positions = self.mobs_positions2
        elif self.maze == self.maze3:
            self.mobs = self.mobs3
            self.mobs_positions = self.mobs_positions3

    def get_current_maze_index(self):
        return self.current_maze_index

    def check_player_position_cell_value(self):
        cell_value = self.maze.maze[self.player.position.y][self.player.position.x]
        if abs(cell_value - 0.75) < 1e-6:
            print("0.75")
            return 0.75
        elif abs(cell_value - 0.6) < 1e-6:
            print("0.6")
            return 0.6
        return None

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
        if self.player.position == Position(self.maze.height - 2, self.maze.width - 3):
            if not self.mazes_to_visit:
                # Player reached the end of the last maze
                return "Win"
            else:
                # Player reached the end of the current maze, switch to the next one
                self.switch_to_next_maze()
                return None
        elif self.lives <= 0:
            # Player has no remaining lives
            return "Lose"
        else:
            # Game is not over yet
            return None
    def should_ask_trivia_question(self):
        return self.trivia_question_timer >= self.trivia_question_interval

    def answer_trivia_question_correctly(self):
        self.score += 10
        self.trivia_question_timer = 0

    def answer_trivia_question_incorrectly(self):
        self.score -= 5
        self.trivia_question_timer = 0
        self.lives -= 1

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
            'mobs1': self.mobs1,
            'mobs2': self.mobs2,
            'mobs3': self.mobs3,
            'mobs4': self.mobs4,
            'mobs_positions1': self.mobs_positions1,
            'mobs_positions2': self.mobs_positions2,
            'mobs_positions3': self.mobs_positions3,
            'mobs_positions4': self.mobs_positions4,
            'visited_mazes': self.visited_mazes,
            'mazes_to_visit': self.mazes_to_visit,
            'player': self.player,
            'mobs': self.mobs,
            'mobs_positions': self.mobs_positions,
            'score': self.score,
            'difficulty_level': self.difficulty_level,
            'num_mobs': self.num_mobs,
            'mob_data': mob_data,  # Include mob_data in the game state
            'cell_size': self.cell_size,
            'lives': self.lives,
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
            self.mobs1 = game_state['mobs1']
            self.mobs2 = game_state['mobs2']
            self.mobs3 = game_state['mobs3']
            self.mobs4 = game_state['mobs4']
            self.mobs_positions1 = game_state['mobs_positions1']
            self.mobs_positions2 = game_state['mobs_positions2']
            self.mobs_positions3 = game_state['mobs_positions3']
            self.mobs_positions4 = game_state['mobs_positions4']
            self.visited_mazes = game_state['visited_mazes']
            self.mazes_to_visit = game_state['mazes_to_visit']
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
            self.lives = game_state['lives']