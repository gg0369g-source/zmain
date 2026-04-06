import os
import sys

print("=" * 50)
print("ИНФОРМАЦИЯ ОБ ОКРУЖЕНИИ")
print("=" * 50)
print(f"Исполняемый файл Python: {sys.executable}")
print(f"Версия Python: {sys.version}")

# Проверка Pillow с корректным атрибутом
try:
    from PIL import Image, ImageTk
    print(f"✅ Pillow успешно импортирован. Версия: {Image.__version__}")

    # Тест создания изображения
    test_img = Image.new('RGB', (50, 50), color='green')
    test_img.save('validator_test.png')
    print("✅ Тест Pillow пройден: создано тестовое изображение")
    VALIDATION_PASSED = True
except ImportError as e:
    print(f"❌ Ошибка импорта Pillow: {e}")
    print("Проверьте установку Pillow: pip install Pillow")
    VALIDATION_PASSED = False
except AttributeError as e:
    print(f"❌ Неожиданная ошибка атрибута: {e}")
    VALIDATION_PASSED = False
except Exception as e:
    print(f"❌ Ошибка при тестировании Pillow: {e}")
    VALIDATION_PASSED = False

if not VALIDATION_PASSED:
    sys.exit(1)

print("\n✅ Все проверки пройдены успешно!")
print("Теперь можно запускать main.py")
