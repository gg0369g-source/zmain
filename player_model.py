class PlayerModel:
    def __init__(self, texture_manager):
        self.texture_manager = texture_manager
        self.current_texture = "player_idle"
        self.animation_frames = {
            "idle": ["player_idle"],
            "walk": ["player_walk1", "player_walk2"],
            "jump": ["player_jump"]
        }
        self.frame_index = 0
        self.animation_speed = 0.2

    def update_animation(self, state="idle"):
        """Обновляет анимацию в зависимости от состояния"""
        frames = self.animation_frames.get(state, ["player_idle"])
        self.frame_index = (self.frame_index + self.animation_speed) % len(frames)
        frame_name = frames[int(self.frame_index)]
        self.current_texture = frame_name

    def draw(self, canvas, x, y, block_size):
        """Отрисовывает игрока с текущей текстурой"""
        texture = self.texture_manager.get_texture(self.current_texture)
        if texture:
            canvas.create_image(
                x * block_size + block_size // 2,
                y * block_size + block_size // 2,
                image=texture,
                anchor='center'
            )
        else:
            # Резервная отрисовка, если текстура не найдена
            canvas.create_oval(
                x * block_size + 2, y * block_size + 2,
                (x + 1) * block_size - 2, (y + 1) * block_size - 2,
                fill='red', outline='black'
            )
