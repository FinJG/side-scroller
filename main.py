import sys

import pygame

from player import Player
from world import World
import sprite_handler

pygame.init()

# Constants
WIDTH, HEIGHT = SCREEN_SIZE = 768, 768
FPS = 60

# Load images
sprite_handler.load_animation("sprites/player/walking_right", 0.3)
sprite_handler.load_animation("sprites/player/walking_left", 0.3)
sprite_handler.load_animation("sprites/player/idle", 1)
sprite_handler.load_animation("sprites/player/breaking_right", 0.1)


# Variables
screen = pygame.display.set_mode(SCREEN_SIZE)
display = pygame.Surface((300, 300))
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
    player.grid_x = player.rect.x // world.tile_size + world.rendering_x
    player.grid_y = player.rect.y // world.tile_size + world.rendering_y
    
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
    
    collision_tiles = []
    tile_size = world.tile_size

    # get tiles to render
    rendering = world.get_rendering()

    # draw tiles being rendered
    for ix, x in enumerate(rendering):
        for iy, y in enumerate(x):

            # draw dirt
            if y == 1: 
                display.blit(sprite_handler.dirt_1, (ix * tile_size, iy * tile_size))

            # draw grass
            elif y == 2:
                surrounding = check_neighbours(ix + world.rendering_x, iy + world.rendering_y, [1, 2])

                # turn grass into dirt if grass is surrounded by tiles
                if surrounding == (True, True, True, True): 
                    rendering[ix, iy] = 1
                    display.blit(sprite_handler.dirt_1, (ix * tile_size, iy * tile_size))

                else:
                    display.blit(sprite_handler.grass_images.get(surrounding, sprite_handler.grass_images[(False, False, False, False)]), (ix * tile_size, iy * tile_size))
            
            if y != 0:
                collision_tiles.append(pygame.Rect(ix * tile_size, iy * tile_size, tile_size, tile_size))


    # break tiles
    if pygame.mouse.get_pressed()[0]:
        player.breaking = True
        x, y = pygame.mouse.get_pos()
        multiplier = WIDTH / display.get_width()
        x = int((x / multiplier) // tile_size) + world.rendering_x
        y = int((y / multiplier) // tile_size) + world.rendering_y
        if (x, y) not in player.get_touching():
            if world.array[x, y] != 0:
                world.array[x, y] = 0

    # place tiles
    if pygame.mouse.get_pressed()[2]:
        player.breaking = True
        x, y = pygame.mouse.get_pos()
        multiplier = WIDTH / display.get_width()
        x = int((x / multiplier) // tile_size) + world.rendering_x
        y = int((y / multiplier) // tile_size) + world.rendering_y
        if (x, y) not in player.get_touching():
            world.array[x, y] = 2


    # update player
    player.update(collision_tiles, dt)

    # draw player
    player.draw(display) 

    # draw display to screen
    screen.blit(pygame.transform.scale(display, SCREEN_SIZE), (0, 0))

    # update screen
    pygame.display.update()
    dt = clock.tick(FPS) / 1000
