import pygame
class Score(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()   
        img_path = 'Sprite/score/score.png'
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)
        