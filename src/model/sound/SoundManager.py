import pygame
# The SoundManager class is responsible for managing sound effects and background music in the game.
class SoundManager:
    """
    The sound manager class for the Python Trivia Maze Game.
    Handles the loading and playback of sound effects and background music.
    """

    # def __init__(self):my
    #     """
    #     Initializes the sound manager.
    #     Loads the sound effects and background music.
    #     """
    #     pygame.mixer.init()
    #     self.sound_effects = self.load_sound_effects()
    #     self.background_music = self.load_background_music()
    #     self.is_music_playing = False

    def load_sound_effects(self):
        """
        Loads the sound effects from files.
        Returns a dictionary mapping sound names to Sound objects.
        """
        sound_effects = {
            "correct_answer": pygame.mixer.Sound("path/to/correct_answer.wav"),
            "incorrect_answer": pygame.mixer.Sound("path/to/incorrect_answer.wav"),
            "game_over": pygame.mixer.Sound("path/to/game_over.wav"),
            "player_move": pygame.mixer.Sound("path/to/player_move.wav"),
            # Add more sound effects here
        }
        return sound_effects

    def load_background_music(self):
        """
        Loads the background music from a file.
        Returns a Sound object.
        """
        background_music = pygame.mixer.Sound("path/to/background_music.mp3")
        return background_music

    def play_sound(self, sound_name):
        """
        Plays a specific sound effect.
        """
        if sound_name in self.sound_effects:
            self.sound_effects[sound_name].play()

    def play_music(self):
        """
        Starts playing the background music in a loop.
        """
        if not self.is_music_playing:
            self.background_music.play(-1)  # -1 means loop indefinitely
            self.is_music_playing = True

    def stop_music(self):
        """
        Stops playing the background music.
        """
        if self.is_music_playing:
            pygame.mixer.music.stop()
            self.is_music_playing = False

    def pause_music(self):
        """
        Pauses the background music.
        """
        if self.is_music_playing:
            pygame.mixer.music.pause()

    def resume_music(self):
        """
        Resumes playing the background music.
        """
        if self.is_music_playing:
            pygame.mixer.music.unpause()

    def set_volume(self, volume):
        """
        Sets the volume for sound effects and background music.
        """
        for sound in self.sound_effects.values():
            sound.set_volume(volume)
        self.background_music.set_volume(volume)