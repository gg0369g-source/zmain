import os
from PIL import Image

class TextureManager:
    def __init__(self, textures_folder="textures"):
        self.textures_folder = textures_folder
        self.pil_textures = {}  # Храним только PIL‑изображения
        self.tk_textures = {}   # Храним Tk‑изображения (создаём после root)
        self.load_pil_textures()

    def load_pil_textures(self):
        """Загружает PIL‑изображения из папки текстур."""
        if not os.path.exists(self.textures_folder):
            print(f"⚠️ Папка '{self.textures_folder}' не найдена. Создаю папку...")
            os.makedirs(self.textures_folder)
            print(f"✅ Папка '{self.textures_folder}' создана.")
            return

        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
        files = os.listdir(self.textures_folder)
        texture_files = [f for f in files if f.lower().endswith(supported_formats)]

        if not texture_files:
            print(f"⚠️ В папке '{self.textures_folder}' нет поддерживаемых изображений.")
            return

        print(f"🔄 Загружаю текстуры из папки '{self.textures_folder}':")

        for filename in texture_files:
            try:
                filepath = os.path.join(self.textures_folder, filename)
                pil_image = Image.open(filepath)
                texture_name = os.path.splitext(filename)[0]

                self.pil_textures[texture_name] = {
                    'pil': pil_image,
            'size': pil_image.size,
            'path': filepath
                }
                print(f"✅ Загружена текстура (PIL): {texture_name} ({pil_image.size[0]}x{pil_image.size[1]})")
            except Exception as e:
                print(f"❌ Ошибка загрузки '{filename}': {e}")


        print(f"🎉 Всего загружено PIL‑текстур: {len(self.pil_textures)}")

    def create_tk_textures(self, root):
        """Создаёт Tk‑изображения после инициализации root."""
        from PIL import ImageTk
        self.tk_textures.clear()
        for name, data in self.pil_textures.items():
            try:
                tk_image = ImageTk.PhotoImage(data['pil'])
                self.tk_textures[name] = tk_image
            except Exception as e:
                print(f"❌ Ошибка создания Tk‑изображения для '{name}': {e}")
        print(f"✅ Создано Tk‑текстур: {len(self.tk_textures)}")

    def get_texture(self, name):
        return self.tk_textures.get(name)

    def get_all_names(self):
        return list(self.pil_textures.keys())

    def print_info(self):
        print("\n📋 ИНФОРМАЦИЯ О ТЕКСТУРАХ:")
        print("-" * 50)
        for name, data in self.pil_textures.items():
            print(f"{name}: {data['size'][0]}x{data['size'][1]} px, {data['path']}")
        print("-" * 50)
