from src.TriviaManager.TriviaManager import TriviaManager


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