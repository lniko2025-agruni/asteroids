import pygame
from sprites.laser import Laser
from config import *
from math import sin, cos, radians


class Player(pygame.sprite.Sprite):
    def __init__(self, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.base_speed = 420
        self.speed = self.base_speed

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.base_cooldown_duration = 500
        self.cooldown_duration = self.base_cooldown_duration
        self.powered_up = False
        self.powerup_end_time = 0

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * dt


        self.rect.centerx = max(0, min(WINDOW_WIDTH, self.rect.centerx))
        self.rect.centery = max(0, min(WINDOW_HEIGHT, self.rect.centery))

        recent_keys = pygame.key.get_just_pressed()

        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()
        if self.powered_up and current_time > self.powerup_end_time:
            self.powered_up = False
            self.cooldown_duration = self.base_cooldown_duration
            self.speed = self.base_speed
        self.laser_timer()

    def shoot(self):
        # center laser
        Laser(
            laser_surf,
            self.rect.midtop,
            pygame.Vector2(0, -1),
            all_sprites,
            laser_sprites,
        ).laser_sound.play()

        if self.powered_up:
            for angle in (-30, 30):
                rad = radians(angle)
                direction = pygame.Vector2(sin(rad), -cos(rad))
                Laser(
                    laser_surf,
                    self.rect.midtop,
                    direction,
                    all_sprites,
                    laser_sprites,
                )
