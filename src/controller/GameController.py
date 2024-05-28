import pygame
from src.model.GameModel import GameModel
from src.view.gameView import GameView


class GameController:
    def __init__(self, game_model, game_view):
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.game_model = GameModel()
        self.game_view = GameView(1280, 720, 11)

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
    cell_size = min(window_width, window_height)  # Adjust the cell size as needed
    game_model = GameModel()
    game_view = GameView(window_width, window_height, cell_size)
    game_controller = GameController(game_model, game_view)
    game_controller.run_game()
