import pygame
from sprites.laser import Laser
from config import *

class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, surf, pos, player_ref, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.player = player_ref

        self.speed = 180
        self.hp = 3

        # shooting
        self.shoot_interval_ms = 700  # fire rate
        self.next_shot_time = pygame.time.get_ticks() + 500  # small delay before first shot

    def damage(self, amount=1):
        self.hp -= amount
        return self.hp <= 0

    def shoot(self):
        # Aim at player (basic homing direction)
        enemy_pos = pygame.Vector2(self.rect.center)
        player_pos = pygame.Vector2(self.player.rect.center)
        direction = player_pos - enemy_pos

        if direction.length_squared() == 0:
            direction = pygame.Vector2(0, 1)
        else:
            direction = direction.normalize()

        laser = Laser(
            enemy_laser_surf,
            self.rect.midbottom,
            direction,
            all_sprites,
            enemy_laser_sprites,
        )

        laser.speed = 330
        laser.laser_sound.play()

    def update(self, dt):
        # Move left -> right
        self.rect.x += self.speed * dt

        now = pygame.time.get_ticks()
        if now >= self.next_shot_time:
            self.shoot()
            self.next_shot_time = now + self.shoot_interval_ms

        if self.rect.left > WINDOW_WIDTH + 80:
            self.kill()
