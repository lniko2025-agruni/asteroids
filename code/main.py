import pygame
from os.path import join
from random import randint, uniform


class Player(pygame.sprite.Sprite):
    def __init__(self, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 400

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

class Star(pygame.sprite.Sprite):
    def __init__(self, surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1080, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Asteroids')
clock = pygame.Clock()

player_surf = pygame.image.load(join('../images', 'player.png')).convert_alpha()
star_surf = pygame.image.load(join('../images', 'star.png')).convert_alpha()

all_sprites = pygame.sprite.Group()
for _ in range(20):
    Star(star_surf, all_sprites)
player = Player(player_surf, all_sprites)

def game_loop():
    running = True

    while running:
        dt = clock.tick() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update(dt)

        display_surface.fill('#111111')
        all_sprites.draw(display_surface)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    game_loop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
