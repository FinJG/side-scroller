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

world[0:WORLD_WIDTH, WORLD_HEIGHT // 4:WORLD_HEIGHT] = 1
world[0:WORLD_WIDTH, WORLD_HEIGHT // 4] = 2

world[5:WORLD_WIDTH // 2, WORLD_HEIGHT // 4] = 0
world[2][12] = 0

dirt_1 = pygame.image.load("sprites/dirt_1.png")

grass_1 = pygame.image.load("sprites/grass/grass_1.png")
grass_left = pygame.image.load("sprites/grass/grass_left.png")
grass_right = pygame.image.load("sprites/grass/grass_right.png")
grass_outside = pygame.image.load("sprites/grass/grass_outside.png")
grass_top = pygame.image.load("sprites/grass/grass_top.png")
grass_pillar = pygame.image.load("sprites/grass/grass_pillar.png")
grass_bottom = pygame.image.load("sprites/grass/grass_bottom.png")
grass_bottom_pillar = pygame.image.load("sprites/grass/grass_bottom_pillar.png")
grass_right_pillar = pygame.image.load("sprites/grass/grass_right_pillar.png")
grass_left_pillar = pygame.image.load("sprites/grass/grass_left_pillar.png")
grass_air = pygame.image.load("sprites/grass/grass_air.png")


def scale_image(image, x, y):
    image_scaled = pygame.transform.scale(image, (tile_size * render_scale_x, tile_size * render_scale_y))
    image_rect = image_scaled.get_rect()
    image_rect.topleft = ((x * tile_size) * render_scale_x, (y * tile_size) * render_scale_y)  
    return image_scaled, image_rect

def check_neighbours(x, y, nums):
    check = [[False, False, False], [False, False, False], [False, False, False]]
    for ix in range(x - 1, x + 2):
        for iy in range(y - 1, y + 2):
            if world[ix, iy] in nums:
                check[ix - x + 1][iy - y + 1] = True
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
    player.update(dt, tile_size, render_scale_x, render_scale_y, world)    

    for ix, x in enumerate(rendering):
        for iy, y in enumerate(x):

            if y == 0:
                pass
            elif y == 1:
                screen.blit(*scale_image(dirt_1, ix, iy))
            elif y == 2:
                surrounding = check_neighbours(ix, iy, (2, 1))

                if not surrounding[0][1] and not surrounding[2][1] and not surrounding[1][0] and not surrounding[1][2]:
                    screen.blit(*scale_image(grass_outside, ix, iy))

                elif surrounding[0][1] and surrounding[1][1] and surrounding[2][1] and not surrounding[1][0] and not surrounding[1][2]:
                    screen.blit(*scale_image(grass_air, ix, iy))

                elif surrounding[0][1] and surrounding[1][1] and surrounding[2][1] and surrounding[1][0]:
                    screen.blit(*scale_image(grass_bottom_pillar, ix, iy)) 

                elif surrounding[0][1] and surrounding[2][1]:
                    screen.blit(*scale_image(grass_1, ix, iy))


                elif surrounding[2][1] and surrounding[1][1] and not surrounding[1][0]:
                    screen.blit(*scale_image(grass_left_pillar, ix, iy))

                elif surrounding[0][1] and surrounding[1][1] and not surrounding[1][2]:
                    screen.blit(*scale_image(grass_right_pillar, ix, iy))
                                      
                elif surrounding[0][1] and not surrounding[2][1] and not surrounding[1][0] and not surrounding[1][2]:
                    screen.blit(*scale_image(grass_right, ix, iy))

                elif surrounding[2][1] and not surrounding[0][1]:
                    screen.blit(*scale_image(grass_left, ix, iy))

                elif surrounding[1][2] and not surrounding[1][0]:
                    screen.blit(*scale_image(grass_top, ix, iy))

                elif surrounding[1][2]:
                    screen.blit(*scale_image(grass_pillar, ix, iy))

                elif surrounding[1][0]:
                    screen.blit(*scale_image(grass_bottom, ix, iy))



                else:
                    screen.blit(*scale_image(grass_1, ix, iy))


    # Draw

    player.draw(screen, render_scale_x, render_scale_y)

    # screen.blit(render_surface, (0, 0))
    # Flip
    pygame.display.update()
    dt = clock.tick(FPS) / 1000
