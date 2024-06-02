import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.button_sound_effect = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "button.mp3"))

    def play_button_sound(self,):
        self.button_sound_effect.play()


