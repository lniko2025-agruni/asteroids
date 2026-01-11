import pygame
from os.path import join


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.smoothscale(surf, (32, 32))
        self.rect = self.image.get_frect(center=pos)

        self.speed = 200  # falling speed
        self.mask = pygame.mask.from_surface(self.image)
        self.power_up_sound = pygame.mixer.Sound(join("audio", "power_up.mp3"))
        self.power_up_sound.set_volume(0.5)

    def update(self, dt):
        self.rect.y += self.speed * dt

        # remove if off screen
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
