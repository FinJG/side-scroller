import sys

import pygame

from player import Player
from world import World
import sprite_handler

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
    player = Player(300, 0)
    world = World(WIDTH, HEIGHT)
    world.generate()

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
                    display.blit(sprite_handler.dirt_1, (iix, iiy))

                # draw grass
                elif y == 2:
                    surrounding = check_neighbours(ix + chunk_start_x , iy + chunk_start_y, [1, 2])

                    # turn grass into dirt if grass is surrounded by tiles
                    if surrounding == (True, True, True, True): 
                        chunk[ix, iy] = 1
                        display.blit(sprite_handler.dirt_1, (iix, iiy))
                    else:
                        display.blit(sprite_handler.grass_images.get(surrounding, sprite_handler.grass_images[(False, False, False, False)]), (iix, iiy))
                if y != 0:
                    collision_tiles.append(pygame.Rect((ix + chunk_start_x) * world.tile_size, iiy, world.tile_size, world.tile_size))
        return collision_tiles

    # Game loop
    while True:
        player.grid_x = player.rect.x // world.tile_size
        player.grid_y = player.rect.y // world.tile_size

        # i really need to get the y axis working
        world.rendering_pos[0] += (player.rect.x - world.rendering_pos[0] - ((display.get_width() / 2) - player.rect.width / 2)) / 10
        # world.rendering_pos[1] += (player.rect.y - world.rendering_pos[1])

        world.scroll = world.rendering_pos.copy()
        world.scroll = [int(i) for i in world.scroll]

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
                    world = World(WIDTH, HEIGHT)
                    player = Player(300, 0)
                    world.generate()
        
        collision_tiles = []

        # draw tiles being rendered
        for jx in range(0, 2):
            for jy in range(0, 2):
                thing = world.CHUNK_SIZE * (jx + (player.grid_x // world.CHUNK_SIZE))
                thing2 = world.CHUNK_SIZE * (jy + (player.grid_y // world.CHUNK_SIZE))
                if jx == 0:
                    collision_tiles = draw_chunk(world.array[thing - world.CHUNK_SIZE:thing, thing2 - world.CHUNK_SIZE:thing2], collision_tiles, thing - world.CHUNK_SIZE, 0)
                collision_tiles = draw_chunk(world.array[thing:world.CHUNK_SIZE + thing,0:world.CHUNK_SIZE + 0], collision_tiles, thing, 0)

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
