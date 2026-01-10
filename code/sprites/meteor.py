import pygame
from random import randint, uniform


class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=pos)

        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(45, 90)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.original_surf, self.rotation)
        self.rect = self.image.get_frect(center=self.rect.center)
