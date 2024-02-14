import pygame
from maze_settings import Width, Height, fps
from Menu import MainMenu

if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 1, 512)

    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    
    clock = pygame.time.Clock()

    main_menu = MainMenu(screen)  

    main_menu.run_menu()

    pygame.display.update()
    clock.tick(fps)
        

