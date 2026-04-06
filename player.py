class Player:
    def __init__(self, world, start_x=12, start_y=10):
        self.world = world
        self.x = start_x
        self.y = start_y
        self.speed = 1

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if self._can_move_to(new_x, new_y):
            self.x, self.y = new_x, new_y

    def _can_move_to(self, x, y):
        return (0 <= x < self.world.width and
                0 <= y < self.world.height and
                not self.world.is_solid(x, y))

    def apply_gravity(self):
        if (self.y < self.world.height - 1 and
            not self.world.is_solid(self.x, self.y + 1)):
            self.y += 1
