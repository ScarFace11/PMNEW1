import pygame
"""
pygame.mixer.music.load("Sounds/Background/BeepBox-Song.waw")
class Music():
    def __init__(self):
        self.music = False

    def Background(self):
        pygame.mixer.music.play(-1)
"""
def Background():
        pygame.mixer.music.load("Sound/Background/BeepBox-Song.wav")
        pygame.mixer.music.play(-1)
def MusicOff():
        pygame.mixer.music.unload()