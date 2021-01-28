#!/usr/bin/env python

"""
Advent of Code day 21 challenge
"""

import sys
from pathlib import Path
from typing import Iterator


# Common -----------------------------------------------------------------------


def load_foods(file: Path) -> Iterator[dict[str, any]]:
    """
    Read foods from the given file

    :param file: file containing list of food with ingredients and allergens
    :return: iterator of dict objects
    """

    line_ending = ')\n'
    for i, line in enumerate(open(file)):
        if not line.endswith(line_ending):
            continue
        groups = line.strip(line_ending).split(' (contains ')
        ingredients = groups[0].split()
        allergens = groups[1].split(', ')
        assert all(map(len, (ingredients, allergens)))
        food: dict = {
            'line': 1 + i,
            'ingredients': ingredients,
            'some_allergens': allergens,
            }
        yield food


def list_safe_ingredients(foods: list[dict[str, any]]) -> set[str]:
    """
    List safe ingredients without allergen

    :param foods: list of ingredients and corresponding known allergens
    :return: list of ingredients which do not contain any allergen
    """

    safe_ingredients = {ingredient
                        for f in foods
                        for ingredient in f['ingredients']}

    ingredients_by_allergen = dict()
    for food in foods:
        ingredients = set(food['ingredients'])
        for allergen in food['some_allergens']:
            if allergen not in ingredients_by_allergen:
                ingredients_by_allergen[allergen] = [ingredients]
            else:
                ingredients_by_allergen[allergen].append(ingredients)

    for allergen, food_ingredients in ingredients_by_allergen.items():
        unsafe_ingredients = set.intersection(*food_ingredients)
        safe_ingredients -= unsafe_ingredients

    return safe_ingredients


def count_ingredients(foods: list[dict[str, any]], ingredient: str) -> int:
    """
    Count number of occurrences of an ingredient in a list of foods

    :param foods: list of ingredients and corresponding known allergens
    :param ingredient: ingredient to count
    :return: number of occurrences
    """

    count = sum(1 for f in foods if ingredient in f['ingredients'])

    return count


def compute_part_one(file: Path) -> int:
    """
    Compute submission value for part one

    :param file:
    :return:
    """

    foods: list = list(load_foods(file=file))
    safe_ingredients = list_safe_ingredients(foods=foods)
    count = lambda i: sum(1 for f in foods if i in f['ingredients'])
    submission = sum(count(i) for i in safe_ingredients)

    return submission


def main() -> int:
    """
    Main function

    :return: shell exit code
    """

    files = [
        './example.txt',
        './input.txt',
    ]
    for f in files:
        print(f'\tPart one, file {f}, submit: {compute_part_one(file=Path(f))}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
