import pygame
from maze_settings import * 
from OpenGame import Main
from AllMazes import *
from Music import *
from copy import deepcopy
def show_level_menu():
    GameMusic.MusicOff()
    pygame.display.set_caption("Меню с выбором уровней")
    

    # Шрифт
    font = pygame.font.Font(None, 36)
    screen = pygame.display.set_mode((Width, Height))

    OpG = Main(screen)
    
    # Класс для уровня
    class Level:
        def __init__(self, image, number, x, y):
            self.screen = screen
            self.image = image
            self.number = number
            self.rect = self.image.get_rect(topleft=(x, y))
            self.default_color = Color_Yellow
            self.hover_color = Color_Purple
            self.text_rect = pygame.Rect(self.rect.centerx, self.rect.bottom + 20, self.rect.width, 30)
            self.hovered = False

        def draw(self):
            pygame.draw.rect(screen, Color_Yellow, self.rect.inflate(10, 10), 6)  # Толстая рамка для изображения уровня
            screen.blit(self.image, self.rect.topleft)
            text_color = Color_Purple if self.hovered else Color_Yellow 
            text = font.render(f"Уровень {self.number}", True, text_color)
            screen.blit(text, self.text_rect)

        def check_hover(self, pos):
            self.hovered = self.rect.collidepoint(pos)

    # Создание объектов уровней с отступами между ними
    level_images = [pygame.image.load(f"Sprite/maze/maze{i}.jpg") for i in range(1, 4)]
    levels = [Level(level_images[i], i + 1, 100 + (i * 250) + (i * 150), 200) for i in range(len(level_images))]

    # Кнопка "выйти"
    exit_button = font.render("Выйти", True, Color_Yellow)
    exit_rect = exit_button.get_rect(center=(Width // 2, Height - 50))
    exit_hovered = False

    dim_color = (0, 0, 0, 150)  # RGBA: четвёртый компонент - прозрачность

    running = True
    while running:
        #screen.fill(Color_Black)
        screen.blit(background_image, (0, 0))  # Отображение фона
        # Отображение затемнённого фона
        dim_surface = pygame.Surface((Width, Height))
        dim_surface.fill(dim_color)
        dim_surface.set_alpha(dim_color[3])
        screen.blit(dim_surface, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for level in levels:
                    if level.rect.collidepoint(mouse_pos):
                        if (level.number == 1):   
                            MazeMask = deepcopy(maze1)
                        elif (level.number == 2):
                            MazeMask = deepcopy(mazeLong)                           
                        elif (level.number == 3):
                            MazeMask = deepcopy(MazeClassicmini1)

                        pygame.display.set_caption(f"Уровень: {level.number}")
                        OpG.main(MazeMask)
                        
                if exit_rect.collidepoint(mouse_pos):
                    running = False
                    from Menu import MainMenu
                    main_menu = MainMenu(screen) 
                    main_menu.run_menu()
        for level in levels:
            level.check_hover(mouse_pos)
            level.draw()

        exit_hovered = exit_rect.collidepoint(mouse_pos)
        
        pygame.draw.rect(screen, exit_hovered, exit_rect, 0)
        exit_color = Color_Purple if exit_hovered else Color_Yellow
        exit_button = font.render("Выйти", True, exit_color)
        screen.blit(exit_button, exit_rect)
        
        pygame.display.flip()


# Проверяем, если файл запускается напрямую, то вызываем функцию show_level_menu()
if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    show_level_menu()