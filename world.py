import random
import math
from blocks import BLOCK_COLORS

class GameWorld:
    def __init__(self, width=25, height=20):
        self.width = width
        self.height = height
        self.world = [[None for _ in range(width)] for _ in range(height)]
        self.generate_world()

    def generate_world(self):
        for x in range(self.width):
            base_height = self.height - 5
            amplitude = 4
            frequency = 0.3
            noise = random.uniform(-1, 1)
            height = int(base_height + amplitude * math.sin(x * frequency) + noise)

            for y in range(self.height):
                if y == height:
                    self.world[y][x] = 'grass'
                elif y > height - 3 and y < height:
                    self.world[y][x] = 'dirt'
                elif y > height - 8 and y < height - 2:
                    self.world[y][x] = 'stone'

    def get_block(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.world[y][x]
        return None

    def set_block(self, x, y, block_type):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.world[y][x] = block_type

    def is_solid(self, x, y):
        block = self.get_block(x, y)
        return block is not None

    def destroy_block(self, x, y):
        self.set_block(x, y, None)

    def place_block(self, x, y, block_type='dirt'):
        if not self.is_solid(x, y):
            self.set_block(x, y, block_type)
            return True
        return False
