import os

import pygame

from src.model.GameMenuModel import GameMenuModel
from src.model.GameModel import GameModel
from src.model.MenuModel import MenuModel
from src.model.sound.SoundManager import SoundManager
from src.view.gameView import GameView
from src.view.menuView import MenuView
from src.view.GameMenuView import InGameMenuView


class GameController:
    def __init__(self, game_model, game_view):
        self.game_model = game_model
        self.game_view = game_view
        self.save_file_name = None
        self.menu_model = GameMenuModel(game_model)
        self.menu_view = None  # Initialize menu_view to None
        self.menu_controller = None
        self.menu_open = False

    def run_game(self):
        pygame.init()  # Initialize Pygame
        screen = pygame.display.set_mode(
            (self.game_view.window_width, self.game_view.window_height))  # Create a window surface
        self.game_model.initialize_game(self.game_view.window_width // self.game_view.cell_size,
                                        self.game_view.window_height // self.game_view.cell_size,
                                        self.game_view.cell_size)
        self.menu_view = InGameMenuView(screen, self.game_view)  # Create the menu_view with the screen
        self.menu_controller = InGameMenuController(self, self.menu_model, self.menu_view)  # Create the menu_controller
        running = True
        if self.game_model.current_filename is not None:
            self.game_model.load_game_state(self.save_file_name)
            self.game_model.update_game_state()
        while running:
            user_input = self.game_view.get_user_input()
            if user_input == "quit":
                running = False
            elif user_input == "show_in_game_menu" and not self.menu_open:  # Add this condition
                self.menu_open = True  # Set menu_open to True
                menu_result = self.menu_controller.show_menu()
                self.menu_open = False  # Set menu_open to False after the menu is closed
                if menu_result == "MainMenu":
                    return "MainMenu"
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

            self.render_game(screen)

        pygame.quit()

    def render_game(self, screen):
        screen.fill(self.game_view.color_bg)
        self.game_view.draw_maze(screen, self.game_model.maze)
        self.game_view.draw_player(screen, self.game_model.player)
        for mob in self.game_model.mobs:
            self.game_view.draw_enemy(screen, mob)
        self.game_view.draw_score(screen, self.game_model.score)
        pygame.display.flip()

    def __del__(self):
        self.game_model.close_trivia_manager()


class MenuController:
    def __init__(self, screen):
        self.model = MenuModel()
        self.view = MenuView(screen, self.model)
        self.sound_manager = SoundManager()

    def run(self):
        saves = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
        self.model.load_save_files(saves)
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
                            self.sound_manager.play_button_sound()
                            show_difficulty_options = True
                            show_save_files = False

                        elif selected_option == 'load_game':
                            self.sound_manager.play_button_sound()
                            show_difficulty_options = False
                            show_save_files = True
                        elif selected_option == 'back':
                            self.sound_manager.play_button_sound()
                            show_difficulty_options = False
                            show_save_files = False
                            scroll_offset = 0
                        elif selected_option in ["Easy", "Medium", "Hard"]:
                            self.sound_manager.play_button_sound()
                            self.model.set_difficulty_level(selected_option)
                            return 'new_game', self.model.difficulty_level
                        elif selected_option in self.model.save_files:
                            self.sound_manager.play_button_sound()
                            return 'load_game', selected_option
                        elif selected_option == 'scroll_up':
                            scroll_offset = max(0, scroll_offset - 1)
                        elif selected_option == 'scroll_down':
                            scroll_offset = min(len(self.model.save_files) - 5, scroll_offset + 1)

            self.view.draw_menu(show_difficulty_options, show_save_files, scroll_offset)

        pygame.quit()
        return None, None


class InGameMenuController:
    def __init__(self, game_controller, model, view):
        self.game_controller = game_controller
        self.model = model
        self.view = view
        self.sound_manager = SoundManager()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.show_menu()

    def show_menu(self):
        while True:
            if self.model.show_help_flag:
                back_rect = self.view.draw_help_popup()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if back_rect.collidepoint(event.pos):
                            self.sound_manager.play_button_sound()
                            self.model.hide_help()
            else:
                self.view.draw_menu(self.model.menu_options)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.sound_manager.play_button_sound()
                        clicked_option = self.view.get_clicked_option(event.pos)
                        self.model.set_selected_option(clicked_option)
                        if clicked_option == "Save":
                            self.sound_manager.play_button_sound()
                            self.model.save_game()
                        elif clicked_option == "Load":
                            self.sound_manager.play_button_sound()
                            self.show_load_popup()
                        elif clicked_option == "Help":
                            self.sound_manager.play_button_sound()
                            self.model.show_help()
                        elif clicked_option == "Back":
                            self.sound_manager.play_button_sound()
                            return
                        elif clicked_option == "Main Menu":
                            self.model.return_to_main_menu()
                            self.sound_manager.play_button_sound()
                            return "MainMenu"
                        elif clicked_option == "Exit Game":
                            pygame.quit()
            if self.model.return_to_main_menu_flag:
                self.model.return_to_main_menu_flag = False
                return "MainMenu"

    def show_load_popup(self):
        while True:
            self.view.draw_load_popup(self.model.game_model.get_save_files())
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_save_file = self.view.get_clicked_save_file(event.pos,
                                                                        self.model.game_model.get_save_files())
                    self.sound_manager.play_button_sound()
                    if clicked_save_file == "Back":
                        self.sound_manager.play_button_sound()
                        return
                    elif clicked_save_file:
                        self.model.load_game(clicked_save_file)
                        self.sound_manager.play_button_sound()
                        return
