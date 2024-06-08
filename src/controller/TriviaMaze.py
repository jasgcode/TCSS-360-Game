import os

import pygame
from src.controller.GameController import GameController
from src.controller.GameController import MenuController
from src.model.GameModel import GameModel
from src.view.gameView import GameView


def main():
    """
    Main function to initialize and run the game.
    """
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Maze Game")

    while True:
        menu_controller = MenuController(screen)
        saves_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
        menu_controller.model.load_save_files(saves_directory)
        action, data = menu_controller.run()

        if action == 'new_game':
            difficulty_level = data
            game_model = GameModel()
            game_model.set_difficulty_level(difficulty_level)
            game_view = GameView(1280, 720, game_model.get_cell_size())
            game_controller = GameController(game_model, game_view)
            game_controller.game_model.set_difficulty_level(difficulty_level)
            save_file_name = game_controller.game_model.generate_save_file_name()
            game_controller.save_file_name = save_file_name
            result = game_controller.run_game()
            if result == "MainMenu":
                continue
        elif action == 'load_game':
            save_file_name = data
            game_model = GameModel()
            save_file_path = os.path.join(saves_directory, save_file_name)
            game_model.load_game_state(save_file_path)
            game_view = GameView(1280, 720, game_model.get_cell_size())
            game_controller = GameController(game_model, game_view)
            game_controller.game_model.load_game_state(save_file_path)
            game_controller.save_file_name = save_file_name
            result = game_controller.run_game()
            if result == "MainMenu":
                continue
        else:
            break

    pygame.quit()


if __name__ == "__main__":
    main()