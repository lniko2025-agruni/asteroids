import pygame
from random import randint
from sprites.meteor import Meteor
from sprites.star import Star
from sprites.player import Player
from sprites.heart import Heart
from sprites.powerUp import PowerUp
from config import *
from math import sin


pygame.init()

pygame.display.set_caption("Asteroids")
clock = pygame.Clock()

for _ in range(20):
    Star(star_surf, all_sprites)
player = Player(player_surf, all_sprites)

heart_width, heart_spacing = 50, 20
player_lives = 3
max_lives = 5  # max lives player can have
hearts = []


def update_hearts():
    global player_lives
    global hearts
    global max_lives

    for heart in hearts:
        heart.kill()
    hearts.clear()

    # draw hearts centered at top
    for i in range(player_lives):
        x = (
            WINDOW_WIDTH
            - (player_lives * heart_width + (player_lives - 1) * heart_spacing)
        ) / 2
        x += i * (heart_width + heart_spacing)
        y = heart_spacing
        hearts.append(Heart(heart_surf, (x, y), False, all_sprites))


update_hearts()


meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 300)


power_up_event = pygame.event.custom_type()
pygame.time.set_timer(power_up_event, 10000)


heart_event = pygame.event.custom_type()
pygame.time.set_timer(heart_event, 8000)

font = pygame.font.Font(None, 40)
score = 0


game_music = pygame.mixer.Sound(join("audio", "loop.mp3"))
game_music.set_volume(0.4)
game_music.play(loops=-1)

explosion_sound = pygame.mixer.Sound(join("audio", "explosion.mp3"))
explosion_sound.set_volume(0.5)

player_damage = pygame.mixer.Sound(join("audio", "player_damage.wav"))
player_damage.set_volume(0.5)


def collision():
    global running
    global score
    global player_lives

    if pygame.sprite.spritecollide(
        player, meteor_sprites, True, pygame.sprite.collide_mask
    ):
        if player_lives > 0:
            player_lives -= 1
            player_damage.play()
            update_hearts()  # refresh displayed hearts

        if player_lives <= 0:
            running = False

    for laser in laser_sprites:
        meteors_hit = pygame.sprite.spritecollide(
            laser, meteor_sprites, True, pygame.sprite.collide_mask
        )
        if meteors_hit:
            laser.kill()
            score += 10
            explosion_sound.play()

    powerups_hit = pygame.sprite.spritecollide(
        player, power_up_sprites, True, pygame.sprite.collide_mask
    )

    for powerup in powerups_hit:
        # apply power-up effect
        player.powered_up = True
        player.cooldown_duration = 150
        player.speed = player.base_speed * 1.5
        player.powerup_end_time = pygame.time.get_ticks() + 4500
        # play sound
        powerup.power_up_sound.play()

    heart_hit = pygame.sprite.spritecollide(
        player, heart_sprites, True, pygame.sprite.collide_mask
    )
    for heart in heart_hit:
        if heart.power_up:  # only falling hearts
            if player_lives < max_lives:
                player_lives += 1
                update_hearts()
            heart.heart_sound.play()


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
            if event.type == power_up_event:
                x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                PowerUp(power_up_surf, (x, y), all_sprites, power_up_sprites)
            if event.type == heart_event:
                x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                Heart(heart_surf, (x, y), True, all_sprites, heart_sprites)

        all_sprites.update(dt)
        collision()
        display_surface.fill("#111111")
        all_sprites.draw(display_surface)
        if player.powered_up:
            pulse = 6 + 12 * abs(sin(pygame.time.get_ticks() * 0.003))
            pygame.draw.circle(
                display_surface,
                (255, 200, 0),
                player.rect.center,
                int(player.rect.width // 2 + pulse),
                2,
            )
        score_update()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game_loop()
