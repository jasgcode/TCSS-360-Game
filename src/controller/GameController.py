import pygame
from src.model.GameModel import GameModel
from src.view.gameView import GameView

from src.model.Maze.Maze import Maze
from src.model.TriviaManager.TriviaManager import TriviaManager


class GameController:
    def __init__(self, game_model, game_view):

        self.game_model = GameModel()
        self.game_view = GameView(800, 600, 20)

    def run_game(self):
        pygame.init()  # Initialize Pygame
        screen = pygame.display.set_mode(
            (self.game_view.window_width, self.game_view.window_height))  # Create a window surface

        self.game_model.initialize_game(self.game_view.window_width // self.game_view.cell_size,
                                        self.game_view.window_height // self.game_view.cell_size,
                                        self.game_view.cell_size)
        self.game_model.set_difficulty_level("Easy")  # Set the difficulty level

        running = True
        while running:
            user_input = self.game_view.get_user_input()
            if user_input == "quit":
                running = False
            elif user_input == "up":
                self.game_model.move_player(GameModel.get_position(0, -1))
            elif user_input == "down":
                self.game_model.move_player(GameModel.get_position(0, 1))
            elif user_input == "left":
                self.game_model.move_player(GameModel.get_position(-1, 0))
            elif user_input == "right":
                self.game_model.move_player(GameModel.get_position(1, 0))

            self.game_model.update_game_state()

            if self.game_model.is_game_over():
                running = False

            self.game_view.render_game(self.game_model, screen)

        pygame.quit()


if __name__ == "__main__":
    window_width, window_height = 800, 600
    cell_size = 20  # Adjust the cell size as needed
    game_model = GameModel()
    game_view = GameView(window_width, window_height, cell_size)
    game_controller = GameController(game_model, game_view)
    game_controller.run_game()
=======
        """
        Initializes the GameController with the game model and view.

        :param game_model: The GameModel object representing the game state and logic.
        :param game_view: The GameView object responsible for rendering the game.
        """
        self.game_model = game_model
        self.game_view = game_view

    def start_game(self):
        """
        Starts the game by initializing the game model and view, and entering the main game loop.
        """
        self.game_model.set_maze(self.create_maze())
        self.game_model.set_trivia_manager(self.create_trivia_manager())
        self.game_view.set_game_model(self.game_model)

        self.game_view.display_main_menu()
        while True:
            # Handle main menu events and actions
            if self.game_view.should_start_game():
                self.run_game_loop()
            elif self.game_view.should_quit_game():
                break
        self.game_view.create_menu()

    def run_game_loop(self):
        """
        Runs the main game loop, handling player actions and updating the game state.
        """
        while not self.game_model.is_game_over():
            self.game_view.render_game()

            # Handle player input and update the game state
            direction = self.game_view.get_player_move()
            self.game_model.move_player(direction)

            self.game_model.handle_trivia_question()

        self.game_view.display_game_over()

    def create_maze(self):
        """
        Creates a new maze object for the game.

        :return: The Maze object representing the game maze.
        """
        # Implement the logic to create a new maze object
        # You can load the maze from a file, generate it randomly, or use a predefined layout
        return Maze()

    def create_trivia_manager(self):
        """
        Creates a new trivia manager object for the game.

        :return: The TriviaManager object managing the trivia questions.
        """
        return TriviaManager("path/to/trivia.db")

    def handle_answer_input(self, question):
        """
        Handles the player's input for answering a trivia question.

        :param question: The question tuple containing the question details.
        :return: The index of the player's selected answer.
        """
        self.game_view.display_trivia_question(question)
        return self.game_view.get_player_answer()

