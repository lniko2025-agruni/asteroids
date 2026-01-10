import pygame
from random import randint
from sprites.meteor import Meteor
from sprites.star import Star
from sprites.player import Player
from config import *


pygame.init()

pygame.display.set_caption("Asteroids")
clock = pygame.Clock()

for _ in range(20):
    Star(star_surf, all_sprites)
player = Player(player_surf, all_sprites)

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


def game_loop():
    running = True

    while running:
        dt = clock.tick() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == meteor_event:
                x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                Meteor(meteor_surf, (x, y), all_sprites, meteor_sprites)

        all_sprites.update(dt)

        display_surface.fill("#111111")
        all_sprites.draw(display_surface)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game_loop()