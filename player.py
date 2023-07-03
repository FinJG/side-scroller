import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))

        self.base_width = self.image.get_width() / 2
        self.base_height = self.image.get_height() /2 
        self.image.fill((255, 10, 20))
        self.rect = self.image.get_rect()
        self.player_movement = [0, 0]
        self.player_y_momentum = 0
        self.air_timer = 0


    def update(self, dt, collision_tiles):


        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.air_timer < 300 * dt:
                self.player_y_momentum = -400 * dt

        player_movement = [0, 0]
        if keys[pygame.K_d]:
            player_movement[0] += 300 * dt
        if keys[pygame.K_a]:
            player_movement[0] -= 300 * dt
        player_movement[1] += self.player_y_momentum
        self.player_y_momentum += 40 * dt
        if self.player_y_momentum > 800 * dt:
            self.player_y_momentum = 800 * dt
        
        player_rect, collisions = self.move(self.rect, player_movement, collision_tiles)

        if collisions['bottom']:
            self.player_y_momentum = 0
            self.air_timer = 0
        else:
            self.air_timer += 1

        if collisions['top']:
            self.player_y_momentum = 0 





    def draw(self, screen, render_scale_x, render_scale_y):
        screen.blit(self.image, ((self.rect.x * render_scale_x), (self.rect.y * render_scale_y) ))


    def collision_test(self, rect, tiles):
        return [tile for tile in tiles if rect.colliderect(tile)]

    def get_touching(self, tile_size):
        tile1 = ((self.rect.x // tile_size), (self.rect.y // tile_size))
        tile2 = (math.ceil(self.rect.x / tile_size), math.ceil(self.rect.y / tile_size))
        tile3 = ((self.rect.x // tile_size), math.ceil(self.rect.y / tile_size))
        tile4 = (math.ceil(self.rect.x / tile_size), (self.rect.y // tile_size))
        return tuple(set([tile1, tile2, tile3, tile4]))

    def move(self, rect, movement, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True

        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True

        return rect, collision_types