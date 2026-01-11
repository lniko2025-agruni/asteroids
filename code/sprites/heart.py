import pygame
from config import *
from os.path import join


class Heart(pygame.sprite.Sprite):
    def __init__(self, surf, position, power_up, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center=position)
        self.power_up = power_up
        self.heart_sound = pygame.mixer.Sound(join("audio", "heart.mp3"))
        self.heart_sound.set_volume(1.5)

    def update(self, dt):
        if not self.power_up:
            return
        self.rect.y += 150 * dt
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
