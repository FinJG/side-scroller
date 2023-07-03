import pygame
import sys
import random
import numpy
import math

from player import Player

pygame.init()

# Constants
WIDTH, HEIGHT = SCREEN_SIZE = 768, 768
FPS = 60

# Variables
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
dt = 0
# Classes


# Pixel array
tile_size = 16
WORLD_WIDTH = WIDTH // tile_size
WORLD_HEIGHT = HEIGHT // tile_size

world = numpy.zeros((WORLD_WIDTH, WORLD_HEIGHT), dtype=int)

world[0:WORLD_WIDTH, WORLD_HEIGHT // 3:WORLD_HEIGHT] = 1
world[0:WORLD_WIDTH, WORLD_HEIGHT // 3] = 2

def check_neighbours(x, y, nums):
    check = [False, False, False, False]
    if world[x - 1, y] in nums:
        check[0] = True
    if world[x, y - 1] in nums:
        check[1] = True        
    if world[x + 1, y] in nums:
        check[2] = True
    if world[x, y + 1] in nums:
        check[3] = True
    return check
            
player = Player()

# Game loop
while True:
    # Event loop
    screen.fill((20, 150, 230))

    rendering_x = 0
    rendering_y = 0
    rendering_width = 16
    rendering_height = 16

    rendering = world[rendering_x:rendering_x + rendering_width, rendering_y:rendering_y + rendering_height]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        x = (x // (tile_size * render_scale_x)) 
        y = (y // (tile_size * render_scale_y))

        world[x, y] = 2

    render_scale_x = math.ceil(WORLD_WIDTH / rendering_width)
    render_scale_y = math.ceil(WORLD_HEIGHT / rendering_height)

    player.resize(tile_size, render_scale_x, render_scale_y)
    player.update(dt, tile_size, world)    

    for ix, x in enumerate(rendering):
        for iy, y in enumerate(x):

            if y == 0:
                pass
            elif y == 1:
                screen.blit(*scale_image(dirt_1, ix, iy))
            elif y == 2:
                surrounding = check_neighbours(ix, iy, (2, 1))
                if grass_images.get(tuple(surrounding)):
                    screen.blit(*scale_image(grass_images.get(tuple(surrounding)), ix, iy))
                else:
                    screen.blit(*scale_image(grass_1, ix, iy))


    # Draw

    player.draw(screen, render_scale_x, render_scale_y)

    # screen.blit(render_surface, (0, 0))
    # Flip
    pygame.display.update()
    dt = clock.tick(FPS) / 1000
