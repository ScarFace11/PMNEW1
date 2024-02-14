import pygame
class Icons(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()   
        img_path = 'Sprite/icons/finish-flag.png'
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)