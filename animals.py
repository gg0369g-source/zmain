import random

class Animal:
    def __init__(self, world, x, y, animal_type="cow"):
        self.world = world
        self.x = x
        self.y = y
        self.type = animal_type
        self.speed = random.uniform(0.1, 0.3)
        self.direction = random.choice([-1, 1])

    def update(self):
        """Обновляет позицию животного"""
        # Случайное изменение направления
        if random.random() < 0.02:
            self.direction *= -1

        new_x = self.x + self.direction * self.speed
        if self.world.is_solid(int(new_x), self.y):
            self.direction *= -1  # Отскок от препятствий
        else:
            self.x = new_x

    def draw(self, canvas, block_size, texture_manager):
        """Отрисовывает животное"""
        texture_name = f"{self.type}_idle"
        texture = texture_manager.get_texture(texture_name)
        if texture:
            canvas.create_image(
                int(self.x) * block_size + block_size // 2,
                self.y * block_size + block_size // 2,
                image=texture,
                anchor='center'
            )
        else:
            # Резервная отрисовка
            colors = {"cow": "brown", "pig": "pink", "sheep": "white"}
            color = colors.get(self.type, "gray")
            canvas.create_oval(
                int(self.x) * block_size + 4, self.y * block_size + 4,
                int(self.x + 1) * block_size - 4, (self.y + 1) * block_size - 4,
                fill=color, outline='black'
            )
