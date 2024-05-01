import pygame

class GameController:
    """
    The main controller class for the Python Trivia Maze Game.
    Handles game flow, user input, and coordinates the game model, view, and other managers.
    """

    def __init__(self):
        """
        Initializes the game controller.
        Sets up the game model, view, trivia manager, sound manager, localization manager, and game clock.
        """
        pygame.init()
        self.game_model = GameModel()
        self.game_view = GameView()
        self.trivia_manager = TriviaManager()
        self.sound_manager = SoundManager()
        self.localization_manager = LocalizationManager()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.is_paused = False

    def start_game(self):
        """
        Starts the game by displaying the main menu and waiting for user input.
        If the user starts the game, selects the difficulty level, initializes the game model, and starts the game loop.
        If the user quits, exits the game.
        """
        self.game_view.display_main_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.select_difficulty_level()
                        self.game_model.initialize_game()
                        self.play_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

    def select_difficulty_level(self):
        """
        Prompts the user to select the difficulty level and sets it in the game model and trivia manager.
        """
        difficulty_level = self.game_view.get_difficulty_level()
        self.game_model.set_difficulty_level(difficulty_level)
        self.trivia_manager.set_difficulty_level(difficulty_level)

    def play_game(self):
        """
        Runs the main game loop.
        Handles events, updates the game state, renders the game, and limits the frame rate.
        Continues until the game is over, then displays the game over screen.
        """
        while not self.game_model.is_game_over():
            self.handle_events()
            self.update_game_state()
            self.render_game()
            self.clock.tick(self.fps)
        self.game_view.display_game_over(self.game_model)
        self.wait_for_key_press()

    def handle_events(self):
        """
        Handles game events such as user input for pausing the game or moving the player.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_game()
                elif not self.is_paused:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.game_model.move_player(Position(0, -1))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.game_model.move_player(Position(0, 1))
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.game_model.move_player(Position(-1, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.game_model.move_player(Position(1, 0))

    def update_game_state(self):
        """
        Updates the game state by updating the game model and checking for trivia questions.
        Only performs updates if the game is not paused.
        """
        if not self.is_paused:
            self.game_model.update_game_state()
            self.check_trivia_question()

    def render_game(self):
        """
        Renders the game by displaying the game view and updating the display.
        If the game is paused, also displays the pause menu.
        """
        self.game_view.display_game(self.game_model)
        if self.is_paused:
            self.game_view.display_pause_menu()
        pygame.display.update()

    def check_trivia_question(self):
        """
        Checks if a trivia question should be asked based on the game model's state.
        If a question is triggered, pauses the game, displays the question, and processes the user's answer.
        Plays sound effects for correct and incorrect answers using the sound manager.
        Resumes the game after the question is answered.
        """
        if self.game_model.should_ask_trivia_question():
            self.pause_game()
            question = self.trivia_manager.get_random_question()
            self.game_view.display_trivia_question(question)
            user_answer = self.game_view.get_user_answer()
            if self.trivia_manager.is_answer_correct(question, user_answer):
                self.game_model.answer_trivia_question_correctly()
                self.sound_manager.play_sound("correct_answer")
            else:
                self.game_model.answer_trivia_question_incorrectly()
                self.sound_manager.play_sound("incorrect_answer")
            self.resume_game()

    def pause_game(self):
        """
        Pauses the game by setting the is_paused flag to True and pausing the background music.
        """
        self.is_paused = True
        self.sound_manager.pause_music()

    def resume_game(self):
        """
        Resumes the game by setting the is_paused flag to False and resuming the background music.
        """
        self.is_paused = False
        self.sound_manager.resume_music()

    def wait_for_key_press(self):
        """
        Waits for the user to press the Enter key before returning to the main menu.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return