import pygame
from sys import exit
from maze_settings import *
from maze import world
#from Levels import *
from Music import *

class Main:
    def __init__(self, screen):
        self.screen = screen          
        self.clock = pygame.time.Clock()
        self.player_event = False
        self.pause_active = False  # Флаг для отслеживания активности режима паузы
        #self.maze = None
        # ������ �������������

    def main(self,mazenum):
        World = world(mazenum, self.screen) #---------
        while True:
            self.screen.fill((35, 45, 60))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Вызываем GamePause только при нажатии Escape
                        #World.GamePause(self.screen)
                        if not World.pause_flag and (not World.scoreall and World.player.sprite.life  > 0):  # Проверяем, нужно ли выходить из GamePause
                            print("всё гу")
                            World.set_Pause_Flag(True)
                            self.pause_active = True  # Устанавливаем флаг активности режима паузы
                        else: 
                            World.set_Pause_Flag(False)   
                            self.pause_active = False 
                        #MusicOff()
                        #from Levels import show_level_menu
                        #show_level_menu()
                        #pygame.quit()
                        #exit()
                    elif self.pause_active:
                        pass
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player_event = 'left'
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player_event = 'right'  
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player_event = 'down'
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player_event = 'up'
                    elif event.key == pygame.K_r:
                        self.player_event = 'restart'
                #elif event.type == pygame.KEYUP and self.player_event == 'boost':
                    #self.player_event = False

             
            World.update(self.screen, self.player_event) #--------

            if (not World.pause_flag):
                self.pause_active = False
            #Menu.menu(self.player_event)         
            pygame.display.update()
            self.clock.tick(fps)