import pygame
import os


class SoundManager:
    def __init__(self):
        """
        Initialize the SoundManager and load the button sound effect.
        """
        pygame.mixer.init()
        self.button_sound_effect = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "button.mp3"))

    def play_button_sound(self,):
        """
        Play the button sound effect.
        """
        self.button_sound_effect.play()


