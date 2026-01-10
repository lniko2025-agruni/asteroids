import pygame
from os.path import join


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)
        self.laser_sound = pygame.mixer.Sound(join("audio", "laser.mp3"))
        self.laser_sound.set_volume(0.5)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
