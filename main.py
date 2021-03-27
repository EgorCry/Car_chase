import pygame
import sys
import random
from pygame.locals import *

# Initialize the program
pygame.init()

# Set FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Set colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Setup 400x600 pixels display with caption
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption('Car chase')


class Rival(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Sprites/Enemy.png')
        self.surf = pygame.Surface((50, 80))
        self.rect = self.surf.get_rect(center=(random.randint(40, 360), 0))

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Set game loop
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    FramePerSec.tick(FPS)