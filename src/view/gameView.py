import pygame

class GameView:
    """
    The view class for the Python Trivia Maze Game.
    Handles rendering the game state, displaying menus, and user interface elements.
    """

    def __init__(self):
        """
        Initializes the game view.
        Sets up the game window, fonts, and colors.
        """
        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Python Trivia Maze Game")
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.color_white = (255, 255, 255)
        self.color_black = (0, 0, 0)
        self.color_gray = (128, 128, 128)
        self.color_red = (255, 0, 0)
        self.color_green = (0, 255, 0)

    def display_main_menu(self):
        """
        Displays the main menu screen.
        Shows the game title and instructions to start or quit the game.
        """
        self.window.fill(self.color_black)
        title_text = self.font_large.render("Python Trivia Maze Game", True, self.color_white)
        start_text = self.font_medium.render("Press Enter to Start", True, self.color_white)
        quit_text = self.font_small.render("Press Esc to Quit", True, self.color_gray)
        self.window.blit(title_text, (self.window_width // 2 - title_text.get_width() // 2, 100))
        self.window.blit(start_text, (self.window_width // 2 - start_text.get_width() // 2, 300))
        self.window.blit(quit_text, (self.window_width // 2 - quit_text.get_width() // 2, 400))
        pygame.display.update()

    def get_difficulty_level(self):
        """
        Displays the difficulty level selection screen and returns the selected difficulty level.
        """
        difficulty_levels = ["Easy", "Medium", "Hard"]
        selected_level = 0
        while True:
            self.window.fill(self.color_black)
            title_text = self.font_large.render("Select Difficulty Level", True, self.color_white)
            self.window.blit(title_text, (self.window_width // 2 - title_text.get_width() // 2, 100))
            for i, level in enumerate(difficulty_levels):
                color = self.color_green if i == selected_level else self.color_white
                level_text = self.font_medium.render(level, True, color)
                self.window.blit(level_text, (self.window_width // 2 - level_text.get_width() // 2, 250 + i * 50))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_level = (selected_level - 1) % len(difficulty_levels)
                    elif event.key == pygame.K_DOWN:
                        selected_level = (selected_level + 1) % len(difficulty_levels)
                    elif event.key == pygame.K_RETURN:
                        return difficulty_levels[selected_level]

    def display_game(self, game_model):
        """
        Displays the game screen with the maze, player, and other game elements.
        """
        self.window.fill(self.color_black)
        self.draw_maze(game_model.maze)
        self.draw_player(game_model.player)
        self.draw_score(game_model.score)
        self.draw_timer(game_model.timer)
        pygame.display.update()

    def draw_maze(self, maze):
        """
        Draws the maze on the game screen.
        """
        cell_size = 20
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell.is_wall():
                    pygame.draw.rect(self.window, self.color_white, (x * cell_size, y * cell_size, cell_size, cell_size))

    def draw_player(self, player):
        """
        Draws the player on the game screen.
        """
        cell_size = 20
        pygame.draw.circle(self.window, self.color_red, (player.position.x * cell_size + cell_size // 2, player.position.y * cell_size + cell_size // 2), cell_size // 2)

    def draw_score(self, score):
        """
        Draws the player's score on the game screen.
        """
        score_text = self.font_small.render(f"Score: {score}", True, self.color_white)
        self.window.blit(score_text, (10, 10))

    def draw_timer(self, timer):
        """
        Draws the game timer on the game screen.
        """
        timer_text = self.font_small.render(f"Time: {timer}", True, self.color_white)
        self.window.blit(timer_text, (self.window_width - timer_text.get_width() - 10, 10))

    def display_trivia_question(self, question):
        """
        Displays a trivia question on the game screen.
        """
        self.window.fill(self.color_black)
        question_text = self.font_medium.render(question.text, True, self.color_white)
        self.window.blit(question_text, (self.window_width // 2 - question_text.get_width() // 2, 100))
        for i, choice in enumerate(question.choices):
            choice_text = self.font_small.render(f"{i + 1}. {choice}", True, self.color_white)
            self.window.blit(choice_text, (100, 200 + i * 50))
        pygame.display.update()

    def get_user_answer(self):
        """
        Retrieves the user's answer to the trivia question.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    elif event.key == pygame.K_2:
                        return 2
                    elif event.key == pygame.K_3:
                        return 3
                    elif event.key == pygame.K_4:
                        return 4

    def display_pause_menu(self):
        """
        Displays the pause menu screen.
        """
        pause_text = self.font_large.render("Paused", True, self.color_white)
        resume_text = self.font_medium.render("Press Enter to Resume", True, self.color_white)
        quit_text = self.font_small.render("Press Esc to Quit", True, self.color_gray)
        self.window.blit(pause_text, (self.window_width // 2 - pause_text.get_width() // 2, 100))
        self.window.blit(resume_text, (self.window_width // 2 - resume_text.get_width() // 2, 300))
        self.window.blit(quit_text, (self.window_width // 2 - quit_text.get_width() // 2, 400))
        pygame.display.update()

    def display_game_over(self, game_model):
        """
        Displays the game over screen with the player's score.
        """
        self.window.fill(self.color_black)
        game_over_text = self.font_large.render("Game Over", True, self.color_white)
        score_text = self.font_medium.render(f"Your Score: {game_model.score}", True, self.color_white)
        self.window.blit(game_over_text, (self.window_width // 2 - game_over_text.get_width() // 2, 100))
        self.window.blit(score_text, (self.window_width // 2 - score_text.get_width() // 2, 300))
        pygame.display.update()