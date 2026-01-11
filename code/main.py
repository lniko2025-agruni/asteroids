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
player = None

meteor_event = pygame.event.custom_type()
power_up_event = pygame.event.custom_type()
heart_event = pygame.event.custom_type()

def enable_game_timers():
    pygame.time.set_timer(meteor_event, 300)
    pygame.time.set_timer(power_up_event, 10000)
    pygame.time.set_timer(heart_event, 8000)

def disable_game_timers():
    pygame.time.set_timer(meteor_event, 0)
    pygame.time.set_timer(power_up_event, 0)
    pygame.time.set_timer(heart_event, 0)

heart_width, heart_spacing = 50, 20
player_lives = 3
max_lives = 5
hearts = []

font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 84)
score = 0

game_music = pygame.mixer.Sound(join("audio", "loop.mp3"))
game_music.set_volume(0.4)
game_music.play(loops=-1)

explosion_sound = pygame.mixer.Sound(join("audio", "explosion.mp3"))
explosion_sound.set_volume(0.5)

player_damage = pygame.mixer.Sound(join("audio", "player_damage.wav"))
player_damage.set_volume(0.5)


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
        y = heart_spacing * 2 
        hearts.append(Heart(heart_surf, (x, y), False, all_sprites))


def score_update():
    global text_surf
    text_surf = font.render(str(score), True, (240, 0, 0))
    text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 30))
    display_surface.blit(text_surf, text_rect)


def draw_centered(text, y, font_obj, color=(240, 240, 240)):
    surf = font_obj.render(text, True, color)
    rect = surf.get_frect(midtop=(WINDOW_WIDTH / 2, y))
    display_surface.blit(surf, rect)


def collision():
    global score
    global player_lives

    if pygame.sprite.spritecollide(
        player, meteor_sprites, True, pygame.sprite.collide_mask
    ):
        if player_lives > 0:
            player_lives -= 1
            player_damage.play()
            update_hearts()
        
        if player_lives <= 0:
            return True

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
    
    return False


def reset_game():
    global player, score, player_lives

    disable_game_timers()
    pygame.event.clear()

    score = 0
    player_lives = 3

    all_sprites.empty()
    meteor_sprites.empty()
    laser_sprites.empty()
    power_up_sprites.empty()
    heart_sprites.empty()

    for _ in range(20):
        Star(star_surf, all_sprites)

    player = Player(player_surf, all_sprites)

    update_hearts()

    enable_game_timers()
    pygame.event.clear([meteor_event, power_up_event, heart_event])


def start_screen():
    disable_game_timers()
    pygame.event.clear()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

        display_surface.fill("#111111")
        draw_centered("ASTEROIDS", 140, big_font, (240, 0, 0))
        draw_centered("Press SPACE to Start", 270, font)
        draw_centered("ESC to Quit", 320, font)
        pygame.display.update()


def game_over_screen(final_score):
    disable_game_timers()
    pygame.event.clear()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return False

        display_surface.fill("#111111")
        draw_centered("GAME OVER", 140, big_font, (240, 0, 0))
        draw_centered(f"Score: {final_score}", 270, font)
        draw_centered("Press R to Restart", 330, font)
        draw_centered("ESC / Q to Quit", 380, font)
        pygame.display.update()


def play_round():
    while True:
        dt = clock.tick() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
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

        dead = collision()
        if dead:
            return False
        
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


def main():
    while True:
        start_ok = start_screen()
        if not start_ok:
            break

        reset_game()
        quit_from_window = play_round()
        if quit_from_window:
            break

        restart = game_over_screen(score)
        if not restart:
            break

    pygame.quit()


if __name__ == "__main__":
    main()