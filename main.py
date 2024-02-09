"""
from maze_settings import *
from maze import world #---------
#from  Menu import Menu
pygame.mixer.pre_init(44100, -16, 1, 512) 
pygame.init()

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Pac-Man")

pygame.mixer.music.load("Sound/Background/BeepBox-Song.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0) #5
BLACK = (0,0,0)
B = (130,40,15)
rgb1 = (151, 126, 188)
rgb2 = (218, 127, 94)
rgb3 = (147, 126, 229)
rgb4 = (35, 45, 60)
class Main:
    def __init__(self,screen):
        self.screen = screen          
        self.clock = pygame.time.Clock()
        self.player_event = False
    def main(self):

        World = world(maze, self.screen) #---------
        while True:
            screen.fill(rgb4)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player_event = 'left'
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player_event = 'right'  
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player_event = 'down'
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player_event = 'up'
                    elif event.key == pygame.K_r :
                        self.player_event = 'restart'
                #elif event.type == pygame.KEYUP:
                    #self.player_event = False

             
            World.update(self.player_event) #--------
            #Menu.menu(self.player_event)         
            pygame.display.update()
            
            
            self.clock.tick(60)

if __name__ == "__main__":
    play = Main(screen)
    play.main()
"""
import pygame
#import sys
from maze_settings import *
#from maze import world
from Menu import MainMenu

#from OpenGame import Main

"""
class Main:
    def __init__(self, screen):
        self.screen = screen          
        self.clock = pygame.time.Clock()
        self.player_event = False
        # Р”СЂСѓРіРёРµ РёРЅРёС†РёР°Р»РёР·Р°С†РёРё

    def main(self):

        World = world(maze, self.screen) #---------
        while True:
            screen.fill((35, 45, 60))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player_event = 'left'
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player_event = 'right'  
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player_event = 'down'
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player_event = 'up'
                    elif event.key == pygame.K_r :
                        self.player_event = 'restart'
                #elif event.type == pygame.KEYUP:
                    #self.player_event = False

             
            World.update(self.player_event) #--------
            #Menu.menu(self.player_event)         
            pygame.display.update()
            self.clock.tick(60)
"""
if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 1, 512)

    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    main_menu = MainMenu(screen)  
    #play = Main(screen)
    show_menu = True  

    while True:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        """
        
        if show_menu:
            main_menu.run_menu()
            show_menu = False

        #elif main_menu.play_game:
            #play.main()

        pygame.display.update()
        clock.tick(fps)
        

