
class GameMenuModel:
    def __init__(self, game_model):
        """
        Initialize the GameMenuModel with the game model.
        """
        self.game_model = game_model
        self.menu_options = ["Save", "Help", "Back", "Main Menu", "Exit Game"]
        self.show = False
        self.selected_option = None
        self.show_help_flag = False
        self.return_to_main_menu_flag = False

    def set_selected_option(self, option):
        """
        Set the selected menu option.
        """

        self.selected_option = option

    def get_selected_option(self):
        """
        Get the selected menu option.
        """
        return self.selected_option

    def save_game(self):
        """
        Save the game state.
        """

        self.game_model.save_game_state(self.game_model.current_filename)

    def load_game(self, file_name):
        """
        Load the game state from the specified file.
        """

        self.game_model.load_game_state(file_name)

    def return_to_main_menu(self):
        """
        Set the flag to return to the main menu.
        """

        self.return_to_main_menu_flag = True

    def show_help(self):
        """
        Show the help menu.
        """
        self.show_help_flag = True

    def hide_help(self):
        """
        Hide the help menu.
        """

        self.show_help_flag = False
