import pygame

dirt_1 = pygame.image.load("sprites/dirt_1.png")

grass_1 = pygame.image.load("sprites/grass/grass_1.png")
grass_left = pygame.image.load("sprites/grass/grass_left.png")
grass_right = pygame.image.load("sprites/grass/grass_right.png")
grass_outside = pygame.image.load("sprites/grass/grass_outside.png")
grass_top = pygame.image.load("sprites/grass/grass_top.png")
grass_pillar = pygame.image.load("sprites/grass/grass_pillar.png")
grass_bottom = pygame.image.load("sprites/grass/grass_bottom.png")
grass_pillar_bottom = pygame.image.load("sprites/grass/grass_pillar_bottom.png")
grass_right_pillar = pygame.image.load("sprites/grass/grass_right_pillar.png")
grass_left_pillar = pygame.image.load("sprites/grass/grass_left_pillar.png")
grass_air = pygame.image.load("sprites/grass/grass_air.png")
grass_cross = pygame.image.load("sprites/grass/grass_cross.png")
grass_pillar_connect_right = pygame.image.load("sprites/grass/pillar_connect_right.png")
player = pygame.image.load("sprites/player/player.png")
grass_right_wall = pygame.image.load("sprites/grass/grass_right_wall.png")
grass_inside = pygame.image.load("sprites/grass/grass_inside.png")
grass_bottom_right = pygame.image.load("sprites/grass/grass_bottom_right.png")
grass_bottom_left = pygame.image.load("sprites/grass/grass_bottom_left.png")
grass_air_bottom = pygame.image.load("sprites/grass/grass_air_bottom.png")
grass_left_wall = pygame.image.load("sprites/grass/grass_left_wall.png")

grass_images = {
    (False, False, False, False): grass_outside,
    (True, False, False, True): grass_right,
    (False, False, True, True): grass_left,
    (False, False, False, True): grass_top,
    (False, True, False, True): grass_pillar,
    (False, True, True, True): grass_left_wall,
    (True, True, True, True): grass_cross,
    (True, True, True, False): grass_air_bottom,
    (True, False, True, False): grass_air,
    (True, False, True, True): grass_1,
    (True, False, False, False): grass_right_pillar,
    (False, False, True, False): grass_left_pillar,
    (False, True, False, False): grass_bottom,
    (True, True, False, True): grass_right_wall,
    (True, True, False, False): grass_bottom_right,
    (False, True, True, False): grass_bottom_left,
}