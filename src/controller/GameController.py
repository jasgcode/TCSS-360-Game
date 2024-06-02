import pygame
from src.model.GameModel import GameModel
from src.model.MenuModel import MenuModel
from src.view.gameView import GameView
from src.view.menuView import MenuView


class GameController:
    def __init__(self, game_model, game_view):
        self.game_model = game_model
        self.game_view = game_view
        self.save_file_name = None

    def run_game(self):
        pygame.init()  # Initialize Pygame
        screen = pygame.display.set_mode(
            (self.game_view.window_width, self.game_view.window_height))  # Create a window surface
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
                    is_correct = self.game_view.show_question_popup(
                        screen,
                        trivia_question.question_text,
                        trivia_question.answer_choices,
                        trivia_question.correct_answer_index
                    )
                    if is_correct:
                        print("Correct answer!")
                        self.game_model.answer_trivia_question_correctly()
                    else:
                        print("Wrong answer!")
                        self.game_model.answer_trivia_question_incorrectly()
                    self.game_model.mobs[mob_index].fight = False
                    self.game_model.remove_mob(mob_index)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:  # Press 'S' key to save the game state
                if self.save_file_name is None:
                    self.save_file_name = self.game_model.generate_save_file_name()
                self.game_model.save_game_state(self.save_file_name)
                print(f"Game state saved to {self.save_file_name}")

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

    def __del__(self):
        self.game_model.close_trivia_manager()


class MenuController:
    def __init__(self, screen):
        self.model = MenuModel()
        self.view = MenuView(screen, self.model)

    def run(self):
        self.model.load_save_files('saves')

        show_difficulty_options = False
        show_save_files = False
        scroll_offset = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        selected_option = self.view.get_selected_option(pos, show_difficulty_options, show_save_files,
                                                                        scroll_offset)
                        if selected_option == 'new_game':
                            show_difficulty_options = True
                            show_save_files = False
                        elif selected_option == 'load_game':
                            show_difficulty_options = False
                            show_save_files = True
                        elif selected_option == 'back':
                            show_difficulty_options = False
                            show_save_files = False
                            scroll_offset = 0
                        elif selected_option in ["Easy", "Medium", "Hard"]:
                            self.model.set_difficulty_level(selected_option)
                            return 'new_game', self.model.difficulty_level
                        elif selected_option in self.model.save_files:
                            return 'load_game', selected_option
                        elif selected_option == 'scroll_up':
                            scroll_offset = max(0, scroll_offset - 1)
                        elif selected_option == 'scroll_down':
                            scroll_offset = min(len(self.model.save_files) - 5, scroll_offset + 1)

            self.view.draw_menu(show_difficulty_options, show_save_files, scroll_offset)

        pygame.quit()
        return None, None
