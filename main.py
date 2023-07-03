import pygame
import sys
import numpy

from player import Player
from world import World

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

player = Player()
world = World(screen)
world.generate()

def check_neighbours(x, y, nums):
    check = [False, False, False, False]
    for i, v in enumerate([[-1, 0], [0, -1], [1, 0], [0, 1]]):
        if world.array[x + v[0], y + v[1]] in nums:
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                world = World(screen)
                world.generate()

    # Update
    rendering = world.get_rendering()
    collision_tiles = []
    tile_size = world.tile_size
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


    player.update(collision_tiles, dt)

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        multiplier = WIDTH / display.get_width()
        x = int((x / multiplier) // tile_size)
        y = int((y / multiplier) // tile_size)
        if (x, y) not in player.get_touching(tile_size):
            world.array[x, y] = 2


    # Draw
    player.draw(display)  
    screen.blit(pygame.transform.scale(display, SCREEN_SIZE), (0, 0))

    # Flip
    pygame.display.update()
    dt = clock.tick(FPS) / 1000
