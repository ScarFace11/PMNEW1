import pygame
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.pos = pos
        self.size = size

    def draw(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft = self.pos)

class Wall(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        img_path = 'Sprite/wall/stone.png'
        self.draw(img_path)

