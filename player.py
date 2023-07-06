import pygame
import sprite_handler

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = sprite_handler.animation_dict["idle"].frames[0]
        self.rect = self.image.get_rect()
        self.player_movement = [0, 0]
        self.player_y_momentum = 0
        self.air_timer = 0
        self.speed = 300
        self.direction = 1
        self.moving = False
        self.breaking = False
        self.grid_x = 0
        self.grid_y = 0


    def update(self, collision_tiles, dt, world):
        keys = pygame.key.get_pressed()

        # jump if player is on ground
        if keys[pygame.K_w]:
            if self.air_timer < 300 * dt:
                self.player_y_momentum = -400 * dt

        self.player_movement = [0, 0]

        self.moving = False
        if keys[pygame.K_d]:
            sprite_handler.animate(self, sprite_handler.animation_dict["walking_right"], dt)
            self.moving = True
            self.player_movement[0] += self.speed * dt
            self.direction = 1
            
        if keys[pygame.K_a]:
            sprite_handler.animate(self, sprite_handler.animation_dict["walking_left"], dt)
            self.moving = True
            self.player_movement[0] -= self.speed * dt
            self.direction = 0

        if not self.moving:
            self.image = sprite_handler.animation_dict["idle"].frames[self.direction]

        # work in progress
        if self.breaking:pass
            # sprite_handler.animate(self, sprite_handler.animation_dict["breaking_right"], dt)

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

        self.breaking = False


    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


    def collision_test(self, tiles):
        return [tile for tile in tiles if self.rect.colliderect(tile)]


    def get_touching(self):
        touching = []

        # loops through coordinates around the player (0,0 is the players pos so 1,0 would be to the right of the player)
        for i in [[0, 0], [0, 1], [1, 1], [1, 0], [0, 2], [-1, 1], [-1, 0]]:

            # adds the of tiles that the player is touching to the list
            touching.append((self.grid_x + i[0], self.grid_y + i[1]))

        # returns a tuple of the coordinates with no duplicates
        return tuple(set(touching))


    # i stole this whole function from dafluffypotato :)
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
    