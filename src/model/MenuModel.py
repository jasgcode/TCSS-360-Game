import os


class MenuModel:
    def __init__(self):
        self.difficulty_level = None
        self.save_files = []

    def set_difficulty_level(self, difficulty_level):
        self.difficulty_level = difficulty_level

    def load_save_files(self, saves_directory):
        if not os.path.exists(saves_directory):
            os.makedirs(saves_directory)
        self.save_files = [file for file in os.listdir(saves_directory) if file.endswith('.pkl')]