import os
from pprint import pprint
from typing import TextIO


class RecipesParseError(Exception):
    pass


class Kitchener:

    def __init__(self, path: str) -> None:
        self.cook_book = {}
        self.path = path

    @classmethod
    def _get_ingredients_amount(cls, recipes: TextIO, dish_name: str) -> int:
        """Считывает из файла и возвращает количество ингредиентов текущего блюда"""
        ingredients_amount = recipes.readline().strip('\n')
        if ingredients_amount.isdigit():
            return int(ingredients_amount)
        else:
            raise RecipesParseError(f'Не удалось определить количество ингредиентов.'
                                    f'Проверьте количество ингредиентов у "{dish_name}"')

    @classmethod
    def _get_ingredients(cls, recipes: TextIO, ingredients_amount: int, dish_name: str) -> list:
        """Считывает из файла и возвращает список ингредиентов текущего блюда"""
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

    @classmethod
    def _get_next_dish_name(cls, recipes: TextIO) -> str:
        """Считывает из файла и возвращает название следующего блюда"""
        dish_name = recipes.readline()
        while dish_name.isspace():
            dish_name = recipes.readline()
        return dish_name.strip('\n')

    @classmethod
    def _add_ingredients_to_shop_list(cls, ingredients: list, shop_lst: dict, persons_num: int) -> None:
        """Добавляет/прибавляет ингредиенты в словарь покупок"""
        for ingredient in ingredients:
            ingredient_name, quantity, measure = (ingredient['ingredient_name'],
                                                  ingredient['quantity'],
                                                  ingredient['measure'])
            upd_ingredient = shop_lst.get(ingredient_name, {})
            upd_ingredient['measure'] = measure
            upd_ingredient['quantity'] = upd_ingredient.get('quantity', 0) + quantity * persons_num
            shop_lst[ingredient_name] = upd_ingredient

    def get_cook_book(self) -> dict:
        """Заполняет и возвращает книгу рецептов на основе файла с рецептами"""
        with open(self.path, encoding='utf-8') as recipes:
            dish_name = recipes.readline().strip('\n')
            while dish_name:
                ingredients_amount = self._get_ingredients_amount(recipes, dish_name)
                ingredients = self._get_ingredients(recipes, ingredients_amount, dish_name)
                self.cook_book[dish_name] = ingredients
                dish_name = self._get_next_dish_name(recipes)

        return self.cook_book

    def get_shop_list_by_dishes(self, dishes_list: list, persons_num: int) -> dict:
        """Составляет и возвращает словарь покупок на основе блюд и количества персон"""
        shop_lst = {}
        for dish in dishes_list:
            ingredients = self.cook_book.get(dish)
            if ingredients:
                self._add_ingredients_to_shop_list(ingredients, shop_lst, persons_num)
            else:
                print(f'Блюдо "{dish}" не найдено в книге рецептов.')
        return shop_lst


if __name__ == '__main__':
    kitchener = Kitchener('recipes.txt')
    cook_book = kitchener.get_cook_book()
    pprint(cook_book)
    shop_list = kitchener.get_shop_list_by_dishes(['Омлет'], 2)
    pprint(shop_list)
