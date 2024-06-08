import os

import pygame

from src.model.GameMenuModel import GameMenuModel
from src.model.GameModel import GameModel
from src.model.MenuModel import MenuModel
from src.model.sound.SoundManager import SoundManager
from src.view.gameView import GameView
from src.view.MazeEndView import MazeEndView

from src.view.menuView import MenuView
from src.view.GameMenuView import InGameMenuView


class GameController:
    def __init__(self, game_model, game_view):
        pygame.mixer.init()
        self.game_model = game_model
        self.game_view = game_view
        self.save_file_name = None
        self.menu_model = GameMenuModel(game_model)
        self.menu_view = None  # Initialize menu_view to None
        self.menu_controller = None
        self.menu_open = False
        self.cheat_counter = 0  # Counter for the cheat code
        self.completed_mazes = 0  # Keep track of completed mazes
        self.maze_end_view = None  # Initialize MazeEndView to None

    def run_game(self):
        screen = pygame.display.set_mode(
            (self.game_view.window_width, self.game_view.window_height))  # Create a window surface
        self.game_model.initialize_game(self.game_view.window_width // self.game_view.cell_size,
                                        self.game_view.window_height // self.game_view.cell_size,
                                        self.game_view.cell_size)
        self.menu_view = InGameMenuView(screen, self.game_view)  # Create the menu_view with the screen
        self.menu_controller = InGameMenuController(self, self.menu_model, self.menu_view)  # Create the menu_controller

        pygame.mixer.music.load("../BackgroundMusic.mp3")
        pygame.mixer.music.play(-1)

        running = True
        if self.game_model.current_filename is not None:
            self.game_model.load_game_state(self.save_file_name)
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
            elif user_input == "c":
                self.cheat_counter += 1
                print(f"'c' pressed. Cheat counter: {self.cheat_counter}")  # Debug statement
                if self.cheat_counter == 1:  # Adjusted for single press
                    self.teleport_to_end_portal()
                    self.cheat_counter = 0
            else:
                if self.cheat_counter > 0:
                    print(f"Cheat counter reset from {self.cheat_counter} to 0.")  # Debug statement
                self.cheat_counter = 0  # Reset the counter if any other key is pressed

            cell_value = self.game_model.check_player_position_cell_value()
            print(f"Cell value: {cell_value}")
            if cell_value == 0.75:
                print("Player stepped on a cell with value 0.75!")


                if self.game_model.current_maze_index == len(self.game_model.visited_mazes) + len(
                        self.game_model.mazes_to_visit) and user_input == "x" and self.game_model.maze.end_pos is False:
                    # Player reached the end of the last maze
                    x = 'Win'
                    print("Congratulations! You won the game!")
                    result = self.show_maze_end_view(x)
                    if result == "MainMenu":
                        return "MainMenu"
                elif user_input == "x":
                    if self.game_model.maze.end_question is True:
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
                                self.game_model.maze.end_question = False
                            else:
                                print("Wrong answer!")
                                self.game_model.answer_trivia_question_incorrectly()
                                self.game_model.maze.end_question = True
                        if self.game_model.maze.end_question is False:
                            print("Switching to next maze")
                            self.game_model.switch_to_next_maze()
                            self.completed_mazes += 1
            elif cell_value == 0.6:
                print("Player stepped on a cell with value 0.6!")
                if user_input == "x":
                    print("Switching to previous maze")
                    self.game_model.switch_to_previous_maze()

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

            game_over = self.game_model.is_game_over()
            if game_over == "Lose":
                x = 'Lose'
                print("Game Over! You lost the game.")
                result = self.show_maze_end_view(x)
                if result == "MainMenu":
                    return "MainMenu"
            self.render_game(screen)
        self.game_model.update_game_state()

        pygame.display.quit()  # Quit the display here to ensure we can reinitialize it later

    def teleport_to_end_portal(self):
        for y in range(self.game_model.maze.height):
            for x in range(self.game_model.maze.width):
                if self.game_model.maze.maze[y, x] == 0.75:  # Find the blue portal (0.75)
                    self.game_model.player.position.x = x
                    self.game_model.player.position.y = y
                    print(f"Teleported player to end portal at ({x}, {y})")  # Debug statement
                    return

    def show_maze_end_view(self, text):
        self.maze_end_view = MazeEndView(self.game_view.screen, self.game_view.window_width,
                                         self.game_view.window_height)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.maze_end_view.button_rect.collidepoint(event.pos):
                            self.maze_end_view = None # Reset the game state
                            return "MainMenu"

            if text == "Win":
                self.maze_end_view.draw()
            elif text == "Lose":
                self.maze_end_view.draw_end()

            pygame.display.flip()

    def reset_game(self):
        self.game_model.lives = 5  # Reset lives to the initial value
        self.game_model.score = 0  # Reset score to 0
        self.game_model.current_maze_index = 0  # Reset the current maze index
        self.game_model.visited_mazes = []  # Clear the visited mazes
        self.game_model.mazes_to_visit = [self.game_model.maze4, self.game_model.maze3,
                                          self.game_model.maze2]  # Reset the mazes to visit
        self.game_model.maze = self.game_model.maze1  # Set the initial maze to maze1
        self.game_model.mobs = self.game_model.mobs1  # Set the initial mobs to mobs1
        self.game_model.mobs_positions = self.game_model.mobs_positions1  # Set the initial mob positions to mobs_positions1

    def render_game(self, screen):
        screen.fill(self.game_view.color_bg)
        maze_number = self.get_current_maze_number()  # Get the current maze number
        self.game_view.draw_maze(screen, self.game_model.maze, maze_number)
        self.game_view.draw_player(screen, self.game_model.player)
        for mob in self.game_model.mobs:
            self.game_view.draw_enemy(screen, mob)
        self.game_view.draw_score(screen, self.game_model.score)
        self.game_view.draw_lives(screen, self.game_model.lives)
        pygame.display.flip()

    def get_current_maze_number(self):
        if self.game_model.maze == self.game_model.maze1:
            return 1
        elif self.game_model.maze == self.game_model.maze2:
            return 2
        elif self.game_model.maze == self.game_model.maze3:
            return 3
        elif self.game_model.maze == self.game_model.maze4:
            return 4
        else:
            return 0

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
                        # Add this code to the run method
                        # Add this code to the run method
                        elif selected_option == 'About':
                            self.view.show_about_popup()
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

    # def show_load_popup(self):
    #     while True:
    #         self.view.draw_load_popup(self.model.game_model.get_save_files())
    #         for event in pygame.event.get():
    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 clicked_save_file = self.view.get_clicked_save_file(event.pos,
    #                                                                     self.model.game_model.get_save_files())
    #                 self.sound_manager.play_button_sound()
    #                 if clicked_save_file == "Back":
    #                     self.sound_manager.play_button_sound()
    #                     return
    #                 elif clicked_save_file:
    #                     self.model.load_game(clicked_save_file)
    #                     self.sound_manager.play_button_sound()
    #                     return
