import pygame
import pygame_menu
from src.model.GameModel import GameModel
from src.model.Player.Player import Position


class GameView:
    def __init__(self, window_width, window_height, cell_size):
        self.model = GameModel()
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        pygame.font.init()  # Initialize Pygame's font subsystem
        self.font = pygame.font.Font(None, 36)
        self.color_bg = (0, 0, 0)
        self.color_wall = (255, 255, 255)
        self.color_player = (255, 0, 0)
        self.color_text = (0, 0, 0)
        self.menu_theme = pygame_menu.themes.THEME_BLUE.copy()
        self.menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        self.menu_theme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        self.menu_theme.title_font_size = 24
        self.menu_theme.widget_font_size = 18
        self.player_speed = 0.1  # Adjust the player's movement speed

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Python Trivia Maze Game")
        clock = pygame.time.Clock()

        self.model.set_difficulty_level("Easy")  # Set the difficulty level before initializing the game
        self.model.initialize_game(self.window_width // self.cell_size, (self.window_height - 30) // self.cell_size,
                                   self.cell_size)

        self.show_start_screen()

    def show_start_screen(self):
        start_menu = pygame_menu.Menu('Python Trivia Maze Game', self.window_width, self.window_height,
                                      theme=self.menu_theme)
        start_menu.add.button('Start Game', self.start_game)
        start_menu.add.button('Settings', self.show_settings_menu)
        start_menu.add.button('Help', self.show_help_menu)
        start_menu.add.button('Quit', pygame_menu.events.EXIT)
        start_menu.mainloop(self.screen)

    def show_game_over_screen(self):
        game_over_menu = pygame_menu.Menu('Game Over', self.window_width, self.window_height,
                                          theme=self.menu_theme)
        game_over_menu.add.label(f'Final Score: {self.model.score}')
        game_over_menu.add.button('Play Again', self.start_game)
        game_over_menu.add.button('Quit', pygame_menu.events.EXIT)
        game_over_menu.mainloop(self.screen)

    def show_settings_menu(self):
        settings_menu = pygame_menu.Menu('Settings', self.window_width, self.window_height, theme=self.menu_theme)
        settings_menu.add.button('Audio Settings', self.audio_settings)
        settings_menu.add.button('Video Settings', self.video_settings)
        settings_menu.add.button('Controls', self.controls)
        settings_menu.add.selector('Difficulty Level ', [('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],
                                   onchange=self.set_difficulty)
        settings_menu.add.button('Back', self.show_start_screen)
        settings_menu.mainloop(self.screen)

    def show_help_menu(self):
        help_menu = pygame_menu.Menu('Help', self.window_width, self.window_height, theme=self.menu_theme)
        help_menu.add.button('How to Play', self.how_to_play)
        help_menu.add.button('Game Rules', self.game_rules)
        help_menu.add.button('About', self.about)
        help_menu.add.button('Back', self.show_start_screen)
        help_menu.mainloop(self.screen)

    def show_file_menu(self):
        file_menu = pygame_menu.Menu('File', self.window_width, self.window_height, theme=self.menu_theme)
        file_menu.add.button('New Game', self.start_game)
        file_menu.add.button('Save Game', self.save_game)
        file_menu.add.button('Load Game', self.load_game)
        file_menu.add.button('Back', self.main_game_loop)
        file_menu.mainloop(self.screen)

    def draw_menu_bar(self):
        menu_bar_height = 30
        menu_bar_rect = pygame.Rect(0, 0, self.window_width, menu_bar_height)
        pygame.draw.rect(self.screen, (128, 128, 128), menu_bar_rect)

        file_menu_text = self.font.render("File", True, (255, 255, 255))
        settings_menu_text = self.font.render("Settings", True, (255, 255, 255))
        help_menu_text = self.font.render("Help", True, (255, 255, 255))

        file_menu_pos = (10, 5)
        settings_menu_pos = (file_menu_pos[0] + file_menu_text.get_width() + 20, 5)
        help_menu_pos = (settings_menu_pos[0] + settings_menu_text.get_width() + 20, 5)

        self.screen.blit(file_menu_text, file_menu_pos)
        self.screen.blit(settings_menu_text, settings_menu_pos)
        self.screen.blit(help_menu_text, help_menu_pos)

    def start_game(self):
        self.main_game_loop()

    def main_game_loop(self):
        running = True
        clock = pygame.time.Clock()
        move_delay = 0.1  # Adjust this value to change the player's speed
        last_move_time = 0

        while running:
            dt = clock.tick(60) / 1000  # Calculate the time elapsed since the last frame

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if mouse_pos[1] < 30:  # Check if the mouse is clicked in the menu bar area
                            if 10 <= mouse_pos[0] < 10 + self.font.size("File")[0]:
                                self.show_file_menu()
                            elif (10 + self.font.size("File")[0] + 20) <= mouse_pos[0] < (10 + self.font.size("File")[0] + 20 + self.font.size("Settings")[0]):
                                self.show_settings_menu()
                            elif (10 + self.font.size("File")[0] + 20 + self.font.size("Settings")[0] + 20) <= mouse_pos[0] < (10 + self.font.size("File")[0] + 20 + self.font.size("Settings")[0] + 20 + self.font.size("Help")[0]):
                                self.show_help_menu()

            if not self.model.is_game_over():
                self.screen.fill(self.color_bg)
                self.draw_maze(self.screen)
                self.draw_player(self.screen)
                self.draw_score(self.screen)
                self.draw_menu_bar()

                current_time = pygame.time.get_ticks() / 1000  # Get the current time in seconds
                if current_time - last_move_time >= move_delay:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        self.model.move_player(Position(0, -1))
                    elif keys[pygame.K_DOWN]:
                        self.model.move_player(Position(0, 1))
                    elif keys[pygame.K_LEFT]:
                        self.model.move_player(Position(-1, 0))
                    elif keys[pygame.K_RIGHT]:
                        self.model.move_player(Position(1, 0))
                    last_move_time = current_time

                self.model.update_game_state()
            else:
                self.show_game_over_screen()

            pygame.display.flip()

    pygame.quit()
    def audio_settings(self):
        # Implement the logic to configure audio settings
        pass

    def video_settings(self):
        # Implement the logic to configure video settings
        pass

    def controls(self):
        # Implement the logic to configure game controls
        pass

    def set_difficulty(self, selected_value, *args):
        self.model.set_difficulty_level(selected_value)

    def how_to_play(self):
        # Implement the logic to display instructions on how to play
        pass

    def game_rules(self):
        # Implement the logic to display the game rules
        pass

    def about(self):
        # Implement the logic to display information about the game
        pass

    def save_game(self):
        # Implement the logic to save the game state
        pass

    def load_game(self):
        # Implement the logic to load a saved game state
        pass

    def draw_maze(self, screen):
        for y in range(self.model.maze.height):
            for x in range(self.model.maze.width):
                if self.model.maze.maze[y, x] == 1:  # Check if the cell is a wall
                    pygame.draw.rect(screen, self.color_wall,
                                     (x * self.cell_size, y * self.cell_size + 30,
                                      self.cell_size, self.cell_size))

    def draw_player(self, screen):
        x, y = self.model.player.position.x, self.model.player.position.y
        pygame.draw.circle(screen, self.color_player,
                           (int(x * self.cell_size + self.cell_size // 2), int(y * self.cell_size + self.cell_size // 2 + 30)),
                           self.cell_size // 2)

    def draw_score(self, screen):
        text = self.font.render(f"Score: {self.model.score}", True, self.color_text)
        screen.blit(text, (10, 40))


if __name__ == "__main__":
    window_width, window_height = 800, 600
    cell_size = 20  # Adjust the cell size as needed
    view = GameView(window_width, window_height, cell_size)
    view.run()