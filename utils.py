def clamp(value, min_val, max_val):
    """Ограничивает значение диапазоном"""
    return max(min_val, min(value, max_val))

def distance(x1, y1, x2, y2):
    """Вычисляет расстояние между двумя точками"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
