import pygame
"""
pygame.mixer.music.load("Sounds/Background/BeepBox-Song.waw")
class Music():
    def __init__(self):
        self.music = False

    def Background(self):
        pygame.mixer.music.play(-1)
"""
class GameMusic:
        """      
        def run_once(f):
            def wrapper(*args, **kwargs):
                    if not wrapper.has_run:
                            wrapper.has_run = True
                            return f(*args, **kwargs)
            wrapper.has_run = False
            return wrapper
        """
        #@run_once
        def Finish():
            pygame.mixer.music.load("Sound/Background/Finish.wav")
            pygame.mixer.music.play(0)
            pygame.mixer.music.set_volume(0.5)
            
            
        """
        P.S Оказывается можно было обойтись и без этого, run_once уже не нужен
        без декоратора @run_once функция Finish будет производиться в цикле бессконечно раз
        для вызова функции используется
        либо #GameMusic.Finish() либо GameMusic.run_once(GameMusic.Finish()) если они вызываются из других файлов

        для вызова:
        #action = GameMusic.run_once(GameMusic.Finish)   
        #action()
        #action.has_run = False
        """
        
        def Background():
                pygame.mixer.music.load("Sound/Background/BeepBox-Song.wav")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)

        #@run_once
        def MusicOff():
                pygame.mixer.music.unload()