import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))#pygame.image.load("sprites/player/player.png")

        self.base_width = self.image.get_width() / 2
        self.base_height = self.image.get_height() /2 
        self.image.fill((255, 10, 20))
        self.rect = self.image.get_rect()
        # self.rect = pygame.Rect(self.rect.x, self.rect.y , 30, 30)
        # self.rect.center = (100, 100)
    
    def resize(self, tile_size, render_scale_x, render_scale_y):
        self.image = pygame.transform.scale(self.image, (self.base_width * render_scale_x, self.base_height * render_scale_y))
 

    def update(self, dt, tile_size, world):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if world[(self.rect.x // tile_size), (self.rect.y // tile_size)] == 0:
                self.rect.x -= 200 * dt
        
        if world[math.ceil(self.rect.x // tile_size), math.ceil(self.rect.y // tile_size)] != 0:
            self.rect.x = ((self.rect.x // tile_size) + 1) * tile_size

        if keys[pygame.K_d]:
            if world[(self.rect.x // tile_size) + 1, (self.rect.y // tile_size)] == 0:
                self.rect.x += 200 * dt
            

        if world[math.ceil(self.rect.x // tile_size), math.ceil(self.rect.y // tile_size)] != 0:
            self.rect.x = self.rect.x // tile_size * tile_size
                
        if keys[pygame.K_w]:
            self.rect.y -= 600 * dt



        if world[(self.rect.x // tile_size), (self.rect.y // tile_size) + 1] == 0:
            
            self.rect.y += 300 * dt
        
        if world[math.ceil(self.rect.x / tile_size), math.ceil(self.rect.y / tile_size)] != 0:
            self.rect.y = self.rect.y // tile_size * tile_size
            

    def draw(self, screen, render_scale_x, render_scale_y):
        screen.blit(self.image, ((self.rect.x * render_scale_x), (self.rect.y * render_scale_y) ))
