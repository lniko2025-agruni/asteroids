import pygame
from config import *


class Heart(pygame.sprite.Sprite):
    def __init__(self, surf, position, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center=position)