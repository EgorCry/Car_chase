import pygame
import sys
import random
import time
import os
from pygame.locals import *

# Initialize the program
pygame.init()

# Initialize and start a background music
pygame.mixer.init()
pygame.mixer.music.load('Sounds/background.wav')
pygame.mixer.music.play(-1, 0, 0)

# Set FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Set colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Screen variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0


# Setting up fonts
font = pygame.font.SysFont('Verdana', 60)
font_small = pygame.font.SysFont('Verdana', 20)
game_over = font.render('Game Over', True, BLACK)

# Setup 400x600 pixels display with caption and white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption('Car chase')


class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('Sprites/AnimatedStreet.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.movingSpeed = 5

    def update(self):
        print('y1', self.bgY1)
        print('Y2', self.bgY2)
        self.bgY1 += self.movingSpeed
        self.bgY2 += self.movingSpeed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    def render(self):
        DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))


class Rival(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Sprites/Enemy.png')
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center=(random.randint(40, SCREEN_WIDTH-40), 0))

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 650:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Sprites/Player.png')
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[K_UP]:
        # self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        # self.rect.move_ip(0, 5)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH-5:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# Set up sprites
P1 = Player()
E1 = Rival()


# Set up background
back_ground = Background()


# Set up sprites groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)


# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


# Set game loop
while True:
    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
            back_ground.movingSpeed += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    back_ground.update()
    back_ground.render()

    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Moves and Re-draw all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # To be run if collusion occurs between Player and Rival
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('Sounds/crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
