import pygame
from os.path import join


WINDOW_WIDTH, WINDOW_HEIGHT = 1080, 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

laser_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()
player_surf = pygame.image.load(join("images", "player.png")).convert_alpha()
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()
heart_surf = pygame.image.load(join("images", "heart.png")).convert_alpha()
power_up_surf = pygame.image.load(join("images", "power_up.png")).convert_alpha()
enemy_ship_surf = pygame.image.load(join("images", "enemy_ship.png")).convert_alpha()
enemy_laser_surf = laser_surf

all_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
power_up_sprites = pygame.sprite.Group()
heart_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
enemy_laser_sprites = pygame.sprite.Group()
