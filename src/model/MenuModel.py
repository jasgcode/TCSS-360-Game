import os
class MenuModel:
    def __init__(self):
        """
        Load the list of save files from the specified directory.
        """
        self.difficulty_level = None
        self.save_files = []

    def set_difficulty_level(self, level):
        """
        Get the difficulty level for the game.
        """
        self.difficulty_level = level

    def load_save_files(self, saves_dir):
        """
        Load the list of save files from the specified directory.
        """
        self.save_files = []
        for filename in os.listdir(saves_dir):
            if filename.endswith('.pkl'):
                self.save_files.append(filename)