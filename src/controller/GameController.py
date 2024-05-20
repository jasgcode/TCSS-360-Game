from src.model.GameModel import GameModel
from src.view.gameView import GameView


class GameController:
    """
    Controls the flow of the game and coordinates the interactions between the game model and view.
    """

    def __init__(self, game_model, game_view):
        """
        Initializes the GameController with the game model and view.

        :param game_model: The GameModel object representing the game state and logic.
        :param game_view: The GameView object responsible for rendering the game.
        """
        self.game_model = game_model
        self.game_view = game_view

    def initialize_game(self, width, height, cell_size):
        return GameModel.initialize_game(self.game_model, width, height, cell_size)

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

    def generate_maze(self, width, height):
        return GameModel.generate_maze(width, height)

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
