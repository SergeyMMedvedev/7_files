import os
from pprint import pprint


class RecipesParseError(Exception):
    pass


class Kitchener:

    def __init__(self, path):
        self.cook_book = {}
        self.path = path

    def get_ingredients_amount(self, recipes, dish_name):
        ingredients_amount = recipes.readline().strip('\n')
        if ingredients_amount.isdigit():
            return int(ingredients_amount)
        else:
            raise RecipesParseError(f'Не удалось определить количество ингредиентов.'
                                    f'Проверьте количество ингредиентов у "{dish_name}"')

    def get_ingredients(self, recipes, ingredients_amount, dish_name):
        ingredients = []
        for _ in range(ingredients_amount):
            ingredients_data = recipes.readline().strip('\n').split(' | ')
            if len(ingredients_data) == 3:
                ingredient_name, quantity, measure = ingredients_data
                ingredients.append({
                    'ingredient_name': ingredient_name,
                    'quantity': int(quantity),
                    'measure': measure,
                })
            else:
                raise RecipesParseError(f'Проверьте правильно ли указаны игредиенты у "{dish_name}"')
        return ingredients

    def get_next_dish_name(self, recipes):
        dish_name = recipes.readline()
        while dish_name.isspace():
            dish_name = recipes.readline()
        return dish_name.strip('\n')

    def create_cook_book(self):

        with open(self.path, encoding='utf-8') as recipes:
            dish_name = recipes.readline().strip('\n')
            while dish_name:
                ingredients_amount = self.get_ingredients_amount(recipes, dish_name)
                ingredients = self.get_ingredients(recipes, ingredients_amount, dish_name)
                self.cook_book[dish_name] = ingredients
                dish_name = self.get_next_dish_name(recipes)


if __name__ == '__main__':
    kitchener = Kitchener('recipes.txt')
    kitchener.create_cook_book()
    cook_book = kitchener.cook_book
    pprint(cook_book)
