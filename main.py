import pygame
import sys
import random
import numpy
import math

from player import Player

import images

pygame.init()

# Constants
WIDTH, HEIGHT = SCREEN_SIZE = 768, 768
FPS = 60

# Variables
screen = pygame.display.set_mode(SCREEN_SIZE)
display = pygame.Surface((512, 512))
clock = pygame.time.Clock()
dt = 0
rendering_x = 0
rendering_y = 0
rendering_width = 16
rendering_height = 16
player = Player()

# Pixel array
tile_size = 32
WORLD_WIDTH = WIDTH // tile_size
WORLD_HEIGHT = HEIGHT // tile_size

world = numpy.zeros((WORLD_WIDTH, WORLD_HEIGHT), dtype=int)

world[0:WORLD_WIDTH, WORLD_HEIGHT // 3:WORLD_HEIGHT] = 1
world[0:WORLD_WIDTH, WORLD_HEIGHT // 3] = 2

def check_neighbours(x, y, nums):
    check = [False, False, False, False]
    for i, v in enumerate([[-1, 0], [0, -1], [1, 0], [0, 1]]):
        if world[x + v[0], y + v[1]] in nums:
            check[i] = True
    return tuple(check)
            
# Game loop
while True:
    display.fill((20, 150, 230))

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    rendering = world[rendering_x:rendering_x + rendering_width, rendering_y:rendering_y + rendering_height]
    collision_tiles = []
    for ix, x in enumerate(rendering):
        for iy, y in enumerate(x):

            if y == 0:
                pass

            elif y == 1:
                display.blit(images.dirt_1, (ix * tile_size, iy * tile_size))
            elif y == 2:
                surrounding = check_neighbours(ix, iy, [1, 2])
                if surrounding == (True, True, True, True):
                    rendering[ix, iy] = 1
                    display.blit(images.dirt_1, (ix * tile_size, iy * tile_size))
                else:
                    display.blit(images.grass_images.get(surrounding, images.grass_inside), (ix * tile_size, iy * tile_size))

            if y != 0:
                collision_tiles.append(pygame.Rect(ix * tile_size, iy * tile_size, tile_size, tile_size))



    # Draw
    display.blit(player.image, (player.rect.x, player.rect.y))   
    screen.blit(pygame.transform.scale(display, SCREEN_SIZE), (0, 0))

    # Flip
    pygame.display.update()
    dt = clock.tick(FPS) / 1000
