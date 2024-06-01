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
    selected_difficulty = menu_controller.run()

    if selected_difficulty:
        game_model = GameModel()
        game_view = GameView(1280, 720, 22)
        game_controller = GameController(game_model, game_view)
        game_controller.game_model.set_difficulty_level(selected_difficulty)
        game_controller.run_game()


if __name__ == "__main__":
    main()
