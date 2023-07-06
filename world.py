import numpy

class World():
    def __init__(self, screen) -> None:
        self.rendering_pos = [0, 0]
        self.rendering_width = 16
        self.rendering_height = 16
        self.CHUNK_SIZE = 16
        self.tile_size = 32
        self.WORLD_WIDTH = (screen.get_width() // self.tile_size) * 10
        self.WORLD_HEIGHT = (screen.get_height() // self.tile_size)
        self.array = numpy.zeros((self.WORLD_WIDTH, self.WORLD_HEIGHT), dtype=int)
        self.scroll = [0, 0]

    def generate(self):
        self.array[0:self.WORLD_WIDTH, self.WORLD_HEIGHT // 4:self.WORLD_HEIGHT] = 1
        self.array[0:self.WORLD_WIDTH, self.WORLD_HEIGHT // 4] = 2

    def get_rendering(self):
        return self.array[self.scroll[0] // self.tile_size:self.scroll[0] // self.tile_size + self.rendering_width, self.scroll[1] // self.tile_size:self.scroll[1] // self.tile_size + self.rendering_height]
    