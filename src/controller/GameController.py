import pygame
from src.model.GameModel import GameModel
from src.view.gameView import GameView

class GameController:
    def __init__(self, game_model, game_view):
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.game_model = GameModel()
        self.game_view = GameView(1280, 720, 25)

    def run_game(self):
        pygame.init()  # Initialize Pygame
        screen = pygame.display.set_mode(
            (self.game_view.window_width, self.game_view.window_height))  # Create a window surface
        self.game_model.set_difficulty_level("Medium")
        self.game_model.initialize_game(self.game_view.window_width // self.game_view.cell_size,
                                        self.game_view.window_height // self.game_view.cell_size,
                                        self.game_view.cell_size)

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

            mob_index = self.game_model.check_mob_encounter()
            if mob_index is not None:
                print("Mob encounter triggered!")
                trivia_question = self.game_model.get_trivia_question()
                if trivia_question:
                    question_text, answer_choices, correct_answer_index = trivia_question
                    is_correct = self.game_view.show_question_popup(screen, question_text, answer_choices,
                                                                    correct_answer_index)
                    if is_correct:
                        print("Correct answer!")
                        self.game_model.answer_trivia_question_correctly()
                    else:
                        print("Wrong answer!")
                        self.game_model.answer_trivia_question_incorrectly()
                    self.game_model.mobs[mob_index].fight = False
                    self.game_model.despawn_mob(mob_index)

            self.game_model.update_game_state()

            if self.game_model.is_game_over():
                running = False

            self.render_game(screen, self.game_model.difficulty_level)

        pygame.quit()

    def render_game(self, screen, difficulty):
        screen.fill(self.game_view.color_bg)
        self.game_view.draw_maze(screen, self.game_model.maze)
        self.game_view.draw_player(screen, self.game_model.player)
        for mob in self.game_model.mobs:
            if mob.fight:
                self.game_view.draw_enemy(screen, mob)
        self.game_view.draw_score(screen, self.game_model.score)
        pygame.display.flip()


if __name__ == "__main__":
    window_width, window_height = 800, 600
    cell_size = min(window_width, window_height)  # Adjust the cell size as needed
    game_model = GameModel()
    game_view = GameView(window_width, window_height, cell_size)
    game_controller = GameController(game_model, game_view)
    game_controller.run_game()
