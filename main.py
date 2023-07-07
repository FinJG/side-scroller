import sys

import pygame

from player import Player
from world import World
import sprite_handler
import time
def main():
    pygame.init()
    

    # Constants
    WIDTH, HEIGHT = SCREEN_SIZE = 960, 960
    FPS = 60

    # Load images
    sprite_handler.load_animation("sprites/player/walking_right", 0.2)
    sprite_handler.load_animation("sprites/player/walking_left", 0.2)
    sprite_handler.load_animation("sprites/player/idle", 1)
    sprite_handler.load_animation("sprites/player/breaking_right", 0.1)

    # Variables
    screen = pygame.display.set_mode(SCREEN_SIZE)
    display = pygame.Surface((512, 512))
    clock = pygame.time.Clock()
    dt = 0
    world = World(WIDTH, HEIGHT, 1024, 32)
    number_of_chunks_x = 32
    number_of_chunks_y = 32


    world = World(WIDTH, HEIGHT, number_of_chunks_x, number_of_chunks_y)
    world.generate()

    player_spawn_x = 32 * world.tile_size
    player_spawn_y = 13 * world.tile_size

    player = Player(player_spawn_x, player_spawn_y) 

    def check_neighbours(x, y, nums):
        check = [False, False, False, False]
        for i, v in enumerate([[-1, 0], [0, -1], [1, 0], [0, 1]]):
            try: # TEMPORARY FIX
                if world.array[x + v[0], y + v[1]] in nums:
                    check[i] = True
            except IndexError:
                pass
        return tuple(check)


    def change_tile(tile):
        player.breaking = True
        x, y = pygame.mouse.get_pos()
        multiplier = WIDTH / display.get_width()

        x = int((x / multiplier + world.scroll[0]) // world.tile_size)
        y = int((y / multiplier + world.scroll[1]) // world.tile_size)
        if (x, y) not in player.get_touching() or tile == 0:
            try:
                world.array[x, y] = tile
            except IndexError:
                pass


    def draw_chunk(chunk, collision_tiles, chunk_start_x=0, chunk_start_y=0):
        for ix, x in enumerate(chunk):
            for iy, y in enumerate(x):
                iix = (ix + chunk_start_x) * world.tile_size - world.scroll[0]
                iiy = (iy + chunk_start_y) * world.tile_size - world.scroll[1]

                # draw dirt
                if y == 1: 
                    dirt = pygame.transform.scale(sprite_handler.dirt_1, (world.tile_size, world.tile_size))
                    display.blit(dirt, (iix, iiy))

                # draw grass
                elif y == 2:
                    surrounding = check_neighbours(ix + chunk_start_x , iy + chunk_start_y, [1, 2])

                    # turn grass into dirt if grass is surrounded by tiles
                    if surrounding == (True, True, True, True): 
                        chunk[ix, iy] = 1
                        display.blit(pygame.transform.scale(sprite_handler.dirt_1, (world.tile_size, world.tile_size)), (iix, iiy))
                    else:
                        grass = pygame.transform.scale(sprite_handler.grass_images.get(surrounding, sprite_handler.grass_images[(False, False, False, False)]), (world.tile_size, world.tile_size))
                        display.blit(grass, (iix, iiy))
                if y != 0:
                    collision_tiles.append(pygame.Rect((ix + chunk_start_x) * world.tile_size, (iy + chunk_start_y) * world.tile_size, world.tile_size, world.tile_size))
        return collision_tiles

    # Game loop
    while True:
       
        player.grid_x = player.rect.x // world.tile_size 
        player.grid_y = player.rect.y // world.tile_size

        # i really need to get the y axis working
        world.rendering_pos[0] += (player.rect.x - world.rendering_pos[0] - ((display.get_width() / 2) - player.rect.width / 2)) / 3
        world.rendering_pos[1] += (player.rect.y - world.rendering_pos[1] - ((display.get_height() / 2) - player.rect.height / 2)) / 3

        world.scroll = world.rendering_pos.copy()
        world.scroll[0] = int(world.scroll[0])
        world.scroll[1] = int(world.scroll[1])

        if world.scroll[0] < 0:
            world.scroll[0] = 0

        if world.scroll[1] < 0:
            world.scroll[1] = 0


        if world.scroll[0] // world.tile_size >= world.width - (display.get_width() // world.tile_size):
            world.scroll[0] = (world.width - (display.get_width() // world.tile_size)) * world.tile_size

        if world.scroll[1] // world.tile_size > world.height - (display.get_height() // world.tile_size):
            world.scroll[1] = (world.height - (display.get_height() // world.tile_size)) * world.tile_size


        # draw sky
        display.fill((20, 150, 230))

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # get key inputs
            if event.type == pygame.KEYDOWN:

                # reset world if r is pressed
                if event.key == pygame.K_r:
                    world = World(number_of_chunks_x, number_of_chunks_y)
                    player = Player(player_spawn_x, player_spawn_y)
                    world.generate()
        
        collision_tiles = []
        # draw tiles being rendered
        for jx in range(-3, 3):
            for jy in range(-3, 3):

                chunk_x = world.CHUNK_SIZE * (jx + player.grid_x // world.CHUNK_SIZE)
                chunk_y = world.CHUNK_SIZE * (jy + player.grid_y // world.CHUNK_SIZE)


                collision_tiles = draw_chunk(world.array[chunk_x:world.CHUNK_SIZE + chunk_x, chunk_y:world.CHUNK_SIZE + chunk_y], collision_tiles, chunk_x, chunk_y)



        # break tiles
        if pygame.mouse.get_pressed()[0]:
            change_tile(0)
        # place tiles
        if pygame.mouse.get_pressed()[2]:
            change_tile(2)

        # update player
        player.update(collision_tiles, dt, world)

        # # draw player
        display.blit(player.image, (player.rect.x - world.scroll[0], player.rect.y - world.scroll[1]))

        # draw display to screen
        screen.blit(pygame.transform.scale(display, SCREEN_SIZE), (0, 0))

        # update screen
        pygame.display.update()
        dt = clock.tick(FPS) / 1000

if __name__ == "__main__":
    main()
