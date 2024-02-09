import pygame
from maze_settings import Height, Width

pygame.font.init()


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 70)
        self.fontExit = pygame.font.SysFont("impact", 40)
        self.message_color = pygame.Color("darkorange")
        
    def show_life(self, player):
        life_size = 40
        img_path = "Sprite/life/heart.png"
        life_image = pygame.image.load(img_path)
        life_image = pygame.transform.scale(life_image, (life_size, life_size))
        #life_rect = life_image.get_rect(topleft = (0,0))
        indent = 0
        for life in range(player.life):
            indent += life_size
            self.screen.blit(life_image, (indent, life_size))
    # когда хп = 0
    def _game_lose(self, player):
        player.game_over = True
        message = self.font.render('You Lose...', True, self.message_color)
        messageExit = self.fontExit.render('Press Esc to exit', True, self.message_color)
        self.screen.blit(message,(Width // 3 + 70, Height // 3 + 70))
        self.screen.blit(messageExit,(Width // 3 + 70, Height // 3 + 170))
        self.ReturnToLevelSelect()

    # когда игрок взял все бонусы
    def _game_win(self, player):
        player.game_over = True
        player.win = True
        message = self.font.render('You Win!!', True, self.message_color)
        messageExit = self.fontExit.render('Press Esc to exit', True, self.message_color)
        self.screen.blit(message,(Width // 3 + 70, Height // 3 + 70))
        self.screen.blit(messageExit,(Width // 3 + 70, Height // 3 + 170))
        self.ReturnToLevelSelect()

        
    
    # проверка победил ли игрок или проиграл
    def game_state(self, player, goal):
        if player.life <= 0:
            self._game_lose(player)
        elif goal:
            self._game_win(player)
            
    
    def ReturnToLevelSelect(self):
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        from Levels import show_level_menu
                        show_level_menu()