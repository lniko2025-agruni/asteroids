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
pygame.time.set_timer(meteor_event, 300)
font = pygame.font.Font(None, 40)
score = 0


game_music = pygame.mixer.Sound(join("audio", "loop.mp3"))
game_music.set_volume(0.4)
game_music.play(loops=-1)

explosion_sound = pygame.mixer.Sound(join("audio", "explosion.mp3"))
explosion_sound.set_volume(0.5)


def collision():
    global running
    global text_surf
    global score
    if pygame.sprite.spritecollide(
        player, meteor_sprites, True, pygame.sprite.collide_mask
    ):
        running = False

    for laser in laser_sprites:
        meteors_hit = pygame.sprite.spritecollide(
            laser, meteor_sprites, True, pygame.sprite.collide_mask
        )
        if meteors_hit:
            laser.kill()
            score += 10
            explosion_sound.play()


def score_update():
    global text_surf
    text_surf = font.render(str(score), True, (240, 0, 0))
    text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 30))
    display_surface.blit(text_surf, text_rect)


def game_loop():
    global running
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
        collision()
        display_surface.fill("#111111")
        all_sprites.draw(display_surface)
        score_update()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game_loop()
