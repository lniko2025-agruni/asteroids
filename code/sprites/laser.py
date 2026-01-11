import pygame
from os.path import join


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, *groups):
        super().__init__(*groups)

        self.original_image = surf
        self.direction = direction.normalize()

        # rotate image to match movement
        angle = self.direction.angle_to(pygame.Vector2(0, -1))  # 0 deg points up
        self.image = pygame.transform.rotate(self.original_image, angle)

        self.rect = self.image.get_frect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 400
        self.laser_sound = pygame.mixer.Sound(join("audio", "laser.mp3"))
        self.laser_sound.set_volume(0.5)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        # remove if off-screen
        if (
            self.rect.bottom < 0
            or self.rect.top > pygame.display.get_surface().get_height()
            or self.rect.left > pygame.display.get_surface().get_width()
            or self.rect.right < 0
        ):
            self.kill()
