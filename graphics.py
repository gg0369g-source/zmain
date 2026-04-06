from blocks import BLOCK_COLORS

class Graphics:
    def __init__(self, canvas, block_size=32):
        self.canvas = canvas
        self.block_size = block_size

    def draw_world(self, world):
        self.canvas.delete('all')
        for y in range(world.height):
            for x in range(world.width):
                block_type = world.get_block(x, y)
                screen_x = x * self.block_size
                screen_y = y * self.block_size

                if block_type:
                    color = BLOCK_COLORS[block_type]
                    self.canvas.create_rectangle(
                screen_x, screen_y,
                screen_x + self.block_size, screen_y + self.block_size,
                fill=color, outline='black', width=1
            )

    def draw_player(self, player):
        screen_x = player.x * self.block_size + 2
        screen_y = player.y * self.block_size + 2
        size = self.block_size - 4
        self.canvas.create_oval(
            screen_x, screen_y,
            screen_x + size, screen_y + size,
            fill='red', outline='black'
        )
