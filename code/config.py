import pygame
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1080, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


laser_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()
player_surf = pygame.image.load(join("images", "player.png")).convert_alpha()
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()


all_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
