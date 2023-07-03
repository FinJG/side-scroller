import pygame
import math
import images

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = images.player_right

        self.base_width = self.image.get_width() / 2
        self.base_height = self.image.get_height() /2 
        # self.image.fill((255, 10, 20))
        self.rect = self.image.get_rect()
        self.player_movement = [0, 0]
        self.player_y_momentum = 0
        self.air_timer = 0


    def update(self, collision_tiles, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.air_timer < 300 * dt:
                self.player_y_momentum = -400 * dt

        self.player_movement = [0, 0]
        if keys[pygame.K_d]:
            self.image = images.player_right
            self.player_movement[0] += 300 * dt
        if keys[pygame.K_a]:
            self.image = images.player_left
            self.player_movement[0] -= 300 * dt

        self.player_movement[1] += self.player_y_momentum
        self.player_y_momentum += 40 * dt
        if self.player_y_momentum > 800 * dt:
            self.player_y_momentum = 800 * dt
        
        collisions = self.move(collision_tiles)

        if collisions['bottom']:
            self.player_y_momentum = 0
            self.air_timer = 0
        else:
            self.air_timer += 1

        if collisions['top']:
            self.player_y_momentum = 0 

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def collision_test(self, tiles):
        return [tile for tile in tiles if self.rect.colliderect(tile)]


    def get_touching(self, tile_size):
        tile1 = ((self.rect.x // tile_size), (self.rect.y // tile_size))
        tile2 = (math.ceil(self.rect.x / tile_size), math.ceil(self.rect.y / tile_size))
        tile3 = ((self.rect.x // tile_size), math.ceil(self.rect.y / tile_size))
        tile4 = (math.ceil(self.rect.x / tile_size), (self.rect.y // tile_size))
        return tuple(set([tile1, tile2, tile3, tile4]))


    def move(self, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        self.rect.x += self.player_movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.player_movement[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.player_movement[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True

        self.rect.y += self.player_movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.player_movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.player_movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True

        return collision_types
    