import sys
import os
import tkinter as tk
from tkinter import ttk

# --- ПРОВЕРКА ЗАВИСИМОСТЕЙ ---
print("🚀 Запуск проверки зависимостей...")
print("=" * 50)
print("ИНФОРМАЦИЯ ОБ ОКРУЖЕНИИ")
print("=" * 50)

# Информация о Python
print(f"Исполняемый файл Python: {sys.executable}")
print(f"Версия Python: {sys.version}")

# Проверка Pillow
try:
    from PIL import Image, ImageTk
    print("✅ Pillow успешно импортирован. Версия:", Image.__version__)

    # Тест Pillow: создаём тестовое изображение
    test_img = Image.new('RGB', (100, 100), color='red')
    test_img.save('test_pillow.png')
    os.remove('test_pillow.png')  # Удаляем тестовый файл
    print("✅ Тест Pillow пройден: создано тестовое изображение")
except ImportError:
    print("❌ Ошибка: Pillow не установлен. Установите через: pip install Pillow")
    sys.exit(1)
except Exception as e:
    print(f"❌ Ошибка при тестировании Pillow: {e}")
    sys.exit(1)

print("\n✅ Все проверки пройдены успешно!")
print("Теперь можно запускать main.py")


# --- ИНИЦИАЛИЗАЦИЯ МЕНЕДЖЕРА ТЕКСТУР ---
print("\n🖼️ Инициализация текстур (PIL)...")
try:
    from texture_manager import TextureManager
    texture_manager = TextureManager()
except ImportError as e:
    print(f"❌ Ошибка импорта TextureManager: {e}")
    print("Убедитесь, что texture_manager.py находится в той же папке")
    sys.exit(1)
except Exception as e:
    print(f"❌ Ошибка при инициализации текстур: {e}")
    sys.exit(1)

# --- ОСНОВНОЙ КОД ПРИЛОЖЕНИЯ ---
print("\n" + "=" * 50)
print("ЗАПУСК ОСНОВНОГО ПРИЛОЖЕНИЯ")
print("=" * 50)

try:
    # 1. Создаём главное окно
    root = tk.Tk()
    root.title("Платформер с текстурами")
    root.geometry("800x600")
    root.configure(bg="lightblue")

    # 2. Создаём Tk‑изображения ПОСЛЕ создания root
    print("🖼️ Создание Tk‑текстур...")
    texture_manager.create_tk_textures(root)
    texture_manager.print_info()

    # --- ИГРОВОЕ ПОЛЕ ---
    canvas = tk.Canvas(root, width=800, height=500, bg="lightgreen", highlightthickness=0)
    canvas.pack(pady=10)

    # --- ИНФОРМАЦИОННАЯ ПАНЕЛЬ ---
    info_panel = tk.Frame(root, bg="white", relief="sunken", bd=2)
    info_panel.pack(side="bottom", fill="x", padx=10, pady=5)

    info_label = tk.Label(
        info_panel,
        text=f"Pillow {Image.__version__} | Python {sys.version.split()[0]} | Текстур: {len(texture_manager.get_all_names())}",
        bg="white",
        font=("Arial", 10)
    )
    info_label.pack(pady=5)

    # --- ИГРОВЫЕ ПЕРЕМЕННЫЕ ---
    player_texture = texture_manager.get_texture("player_idle")
    stone_texture = texture_manager.get_texture("stone")

    if not player_texture:
        print("⚠️ Текстура player_idle не найдена! Используем стандартный квадрат.")
        player_id = canvas.create_rectangle(50, 50, 80, 80, fill="red", tags="player")
    else:
        player_id = canvas.create_image(50, 50, image=player_texture, tags="player")

    # Создаём платформу из камней — каждый блок отдельно, с фиксированным размером
    if stone_texture:
        block_width = 50  # Ширина блока платформы
        block_height = 50  # Высота блока платформы

        for i in range(0, 800, block_width):
            # Масштабируем текстуру камня под размер блока
            pil_stone = texture_manager.pil_textures["stone"]["pil"]
            scaled_pil = pil_stone.resize((block_width, block_height), Image.Resampling.LANCZOS)
            scaled_texture = ImageTk.PhotoImage(scaled_pil)
            canvas.create_image(i, 450, image=scaled_texture, tags="platform")
            # Сохраняем ссылку на текстуру, чтобы она не удалилась сборщиком мусора
            canvas.image = scaled_texture

    # Параметры игрока
    global player_speed, gravity, is_jumping, jump_power, vertical_momentum
    player_speed = 10
    gravity = 2
    is_jumping = False
    jump_power = 20
    vertical_momentum = 0

    # --- УПРАВЛЕНИЕ ---
    def move_left(event=None):
        coords = canvas.coords(player_id)
        if coords[0] > 0:
            canvas.move(player_id, -player_speed, 0)

    def move_right(event=None):
        coords = canvas.coords(player_id)
        if coords[0] < 750:  # Ограничение по ширине
            canvas.move(player_id, player_speed, 0)

    def jump(event=None):
        global is_jumping, vertical_momentum
        if not is_jumping:
            is_jumping = True
            vertical_momentum = -jump_power


    # Привязываем клавиши
    root.bind("<Left>", move_left)
    root.bind("<Right>", move_right)
    root.bind("<space>", jump)
    root.focus_set()  # Фокусируем окно для приёма клавиш


    # --- ФИЗИКА ИГРЫ ---
    def game_loop():
        global vertical_momentum, is_jumping

        # Применяем гравитацию
        canvas.move(player_id, 0, vertical_momentum)
        vertical_momentum += gravity

        # Проверяем столкновение с платформой
        player_coords = canvas.coords(player_id)
        platform_y = 400  # Уровень платформы

        if (player_coords[1] + 30 >= platform_y and  # Нижняя часть игрока коснулась платформы
            player_coords[0] + 30 >= 0 and
            player_coords[0] <= 800):
            if vertical_momentum > 0:  # Если падает
                canvas.coords(player_id, player_coords[0], platform_y - 30)
                vertical_momentum = 0
                is_jumping = False

        # Ограничиваем падение
        if player_coords[1] > 450:
            canvas.coords(player_id, player_coords[0], 420)
            vertical_momentum = 0
            is_jumping = False

        # Повторяем цикл
        root.after(50, game_loop)

    # Запускаем игровой цикл
    game_loop()

    # --- ОСНОВНАЯ КНОПКА ---
    def on_main_button_click():
        texture_names = texture_manager.get_all_names()
        if texture_names:
            print(f"✅ Доступно текстур: {len(texture_names)}")
            print(f"📝 Список: {', '.join(texture_names)}")
        else:
            print("⚠️ Нет загруженных текстур. Добавьте изображения в папку 'textures'")

    main_button = ttk.Button(
        root,
        text="Обновить информацию о текстурах",
        command=on_main_button_click
    )
    main_button.pack(side="bottom", pady=10)

    print("✅ Интерфейс создан успешно")
    print("🎮 Игра запущена! Управление: ← → для движения, ПРОБЕЛ для прыжка")

    # Запускаем главный цикл Tkinter
    root.mainloop()

except ImportError as e:
    print(f"❌ Ошибка импорта библиотек: {e}")
    print("Убедитесь,что все библитеки устанвлены")