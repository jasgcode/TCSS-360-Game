import os

import pygame
from src.controller.GameController import GameController
from src.controller.GameController import MenuController
from src.model.GameModel import GameModel
from src.view.gameView import GameView


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Maze Game")

    menu_controller = MenuController(screen)
    saves_directory = os.path.join(os.path.dirname(__file__), '..', 'saves')
    menu_controller.model.load_save_files(saves_directory)

    while True:
        action, data = menu_controller.run()

        if action == 'new_game':
            difficulty_level = data
            game_model = GameModel()
            game_view = GameView(1280, 720, 22)
            game_controller = GameController(game_model, game_view)
            game_controller.game_model.set_difficulty_level(difficulty_level)
            save_file_name = game_controller.game_model.generate_save_file_name()
            game_controller.save_file_name = save_file_name
            game_controller.run_game()
        elif action == 'load_game':
            save_file_name = data
            game_model = GameModel()
            game_view = GameView(1280, 720, 22)
            game_controller = GameController(game_model, game_view)
            save_file_path = os.path.join(saves_directory, save_file_name)
            game_controller.game_model.load_game_state(save_file_path)
            game_controller.save_file_name = save_file_name
            game_controller.run_game()
        else:
            break

    pygame.quit()


if __name__ == "__main__":
    main()