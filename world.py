import numpy

class World():
    def __init__(self, WIDTH, HEIGHT, number_of_chunks_x=1, number_of_chunks_y=1) -> None:
        self.rendering_pos = [0, 0]
        self.WORLD_WIDTH = WIDTH * number_of_chunks_x
        self.WORLD_HEIGHT = HEIGHT * number_of_chunks_y
        self.rendering_width = 16
        self.rendering_height = 16
        self.CHUNK_SIZE = 8
        self.tile_size = 32
        self.width = (WIDTH // self.tile_size) * number_of_chunks_x
        self.height = (HEIGHT // self.tile_size) * number_of_chunks_y

        self.array = numpy.zeros((self.width, self.height), dtype=int)
        self.scroll = [0, 0]

    def generate(self):
        self.array[0:self.width, self.height // 4:self.height] = 1
        self.array[0:self.width, self.height // 4] = 2

    def get_rendering(self):
        return self.array[self.scroll[0] // self.tile_size:self.scroll[0] // self.tile_size + self.rendering_width, self.scroll[1] // self.tile_size:self.scroll[1] // self.tile_size + self.rendering_height]
    