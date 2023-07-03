import pygame
import numpy


class World():
    def __init__(self, screen) -> None:
        self.rendering_x = 0
        self.rendering_y = 0
        self.rendering_width = 16
        self.rendering_height = 16
        self.tile_size = 32
        self.WORLD_WIDTH = screen.get_width() // self.tile_size
        self.WORLD_HEIGHT = screen.get_height() // self.tile_size

        self.array = numpy.zeros((self.WORLD_WIDTH, self.WORLD_HEIGHT), dtype=int)

    def generate(self):
        self.array[0:self.WORLD_WIDTH, self.WORLD_HEIGHT // 3:self.WORLD_HEIGHT] = 1
        self.array[0:self.WORLD_WIDTH, self.WORLD_HEIGHT // 3] = 2

    def get_rendering(self):
        return self.array[self.rendering_x:self.rendering_x + self.rendering_width, self.rendering_y:self.rendering_y + self.rendering_height]