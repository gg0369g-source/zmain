class CraftingSystem:
    def __init__(self):
        # Рецепты крафта: {результат: [ингредиенты]}
        self.recipes = {
            "wood_planks": ["wood"],
            "stick": ["wood_planks"],
            "pickaxe": ["stick", "stone"],
            "sword": ["stick", "iron"],
            "chest": ["wood_planks", "wood_planks",
                      "wood_planks", "wood_planks"]
        }
        self.inventory = {"wood": 5, "stone": 3}

    def can_craft(self, recipe_name):
        """Проверяет, можно ли создать предмет"""
        if recipe_name not in self.recipes:
            return False

        required = self.recipes[recipe_name]
        for item in required:
            if self.inventory.get(item, 0) < required.count(item):
                return False
        return True

    def craft(self, recipe_name):
        """Создаёт предмет по рецепту"""
        if not self.can_craft(recipe_name):
            return False

        # Удаляем ингредиенты
        required = self.recipes[recipe_name]
        for item in required:
            self.inventory[item] -= 1
            if self.inventory[item] <= 0:
                del self.inventory[item]

        # Добавляем результат
        self.inventory[recipe_name] = self.inventory.get(recipe_name, 0) + 1
        return True

    def show_inventory(self):
        """Показывает инвентарь"""
        print("Инвентарь:")
        for item, count in self.inventory.items():
            print(f"  {item}: {count}")
