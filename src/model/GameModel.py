import random

class GameModel:
    """
    The model class for the Python Trivia Maze Game.
    Represents the game state and manages the game logic.
    """

    def __init__(self):
        """
        Initializes the game model.
        Sets up the maze, player, score, timer, and difficulty level.
        """
        self.maze = None
        self.player = None
        self.score = 0
        self.timer = 0
        self.difficulty_level = None
        self.trivia_question_interval = 0
        self.trivia_question_timer = 0

    def initialize_game(self):
        """
        Initializes the game state.
        Creates a new maze, positions the player at the starting point, and resets the score and timer.
        """
        self.maze = self.generate_maze()
        self.player = Player(Position(0, 0))
        self.score = 0
        self.timer = 0
        self.trivia_question_timer = 0

    def generate_maze(self):
        """
        Generates a new maze based on the difficulty level.
        """
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
        """
        Sets the difficulty level of the game.
        Adjusts the trivia question interval based on the difficulty level.
        """
        self.difficulty_level = difficulty_level
        if difficulty_level == "Easy":
            self.trivia_question_interval = 20
        elif difficulty_level == "Medium":
            self.trivia_question_interval = 15
        else:  # "Hard"
            self.trivia_question_interval = 10

    def update_game_state(self):
        """
        Updates the game state based on the elapsed time.
        Increments the timer and checks if it's time to ask a trivia question.
        """
        self.timer += 1
        self.trivia_question_timer += 1

    def move_player(self, direction):
        """
        Moves the player in the specified direction if the destination cell is walkable.
        """
        new_position = self.player.position + direction
        if self.maze.is_walkable(new_position):
            self.player.move(direction)
            self.score += 1

    def is_game_over(self):
        """
        Checks if the game is over.
        The game is over when the player reaches the goal position.
        """
        return self.player.position == Position(self.maze.width - 1, self.maze.height - 1)

    def should_ask_trivia_question(self):
        """
        Determines if it's time to ask a trivia question based on the trivia question interval.
        """
        return self.trivia_question_timer >= self.trivia_question_interval

    def answer_trivia_question_correctly(self):
        """
        Handles the scenario when the player answers a trivia question correctly.
        Increases the score and resets the trivia question timer.
        """
        self.score += 10
        self.trivia_question_timer = 0

    def answer_trivia_question_incorrectly(self):
        """
        Handles the scenario when the player answers a trivia question incorrectly.
        Decreases the score and resets the trivia question timer.
        """
        self.score -= 5
        self.trivia_question_timer = 0
