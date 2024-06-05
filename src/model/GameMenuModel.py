
class GameMenuModel:
    def __init__(self, game_model):
        self.game_model = game_model
        self.menu_options = ["Save", "Help", "Back", "Main Menu", "Exit Game"]
        self.show = False
        self.selected_option = None
        self.show_help_flag = False
        self.return_to_main_menu_flag = False

    def set_selected_option(self, option):
        self.selected_option = option

    def get_selected_option(self):
        return self.selected_option

    def save_game(self):
        self.game_model.save_game_state(self.game_model.current_filename)

    def load_game(self, file_name):
        self.game_model.load_game_state(file_name)


    def return_to_main_menu(self):
        self.return_to_main_menu_flag = True

    def show_help(self):
        self.show_help_flag = True

    def hide_help(self):
        self.show_help_flag = False
