# trap.py
import pygame
from support import import_sprite

class Trap(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.size = size
        self.blade_img = import_sprite("Sprite/trap/laser")
        self.frame_index = 0
        self.animation_delay = 3
        self.image = self.blade_img[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = pos)
        
    # adds the spinning effect to the Blade trap
    def _animate(self):
        sprites = self.blade_img
        sprite_index = (self.frame_index // self.animation_delay) % len(sprites)
        self.image = sprites[sprite_index]
        self.image = pygame.transform.scale(self.image, (self.size, self.size+10))
        self.frame_index += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.frame_index // self.animation_delay > len(sprites):
            self.frame_index = 0

    # update object position due to world scroll
    def update(self, x_shift, y_shift):
        self._animate()
        self.rect.x += x_shift
        self.rect.y += y_shift