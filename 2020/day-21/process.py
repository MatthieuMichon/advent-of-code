#!/usr/bin/env python

"""
Advent of Code day 21 challenge
"""

import sys
from collections import defaultdict
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
    for line in open(file):
        if not line.endswith(line_ending):
            continue
        groups = line.strip(line_ending).split(' (contains ')
        ingredients = groups[0].split()
        allergens = groups[1].split(', ')
        assert all(map(len, (ingredients, allergens)))
        food: dict = {
            'ingredients': ingredients,
            'some_allergens': allergens,
            }
        yield food


def map_foods_by_allergen(foods: list[dict[str, any]]) -> dict[str, set[str]]:
    """
    Map for each allergen a list of food known to contain it

    :param foods: list of ingredients and corresponding known allergens
    :return: map of food list by allergen
    """

    foods_by_allergen = defaultdict(list)
    for food in foods:
        ingredients = set(food['ingredients'])
        for allergen in food['some_allergens']:
            foods_by_allergen[allergen].append(ingredients)
    return dict(foods_by_allergen)


# Part One Specific ------------------------------------------------------------


def list_safe_ingredients(foods: list[dict[str, any]]) -> set[str]:
    """
    List safe ingredients without allergen

    :param foods: list of ingredients and corresponding known allergens
    :return: list of ingredients which do not contain any allergen
    """

    safe_ingredients = {ingredient
                        for f in foods
                        for ingredient in f['ingredients']}
    for allergen, food_ingredients in map_foods_by_allergen(foods).items():
        unsafe_ingredients = set.intersection(*food_ingredients)
        safe_ingredients -= unsafe_ingredients
    return safe_ingredients


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


# Part Two Specific ------------------------------------------------------------


def map_allergens(foods: list[dict[str, any]]) -> dict[str, str]:
    """
    Map allergens by ingredients

    :param foods: list of ingredients and corresponding known allergens
    :return: map of allergens by ingredient
    """

    dangerous_ingredients = {
        k: set.intersection(*v)
        for k, v in map_foods_by_allergen(foods).items()}
    allergen_map = dict()
    while len(dangerous_ingredients):
        for allergen, suspected_ingredients in dangerous_ingredients.items():
            suspected_ingredients = suspected_ingredients - set(allergen_map.keys())
            assert 0 < len(suspected_ingredients)
            unambiguous_ingredient = 1 == len(suspected_ingredients)
            if unambiguous_ingredient:
                dangerous_ingredient = list(suspected_ingredients)[0]
                allergen_map[dangerous_ingredient] = allergen
        for allergen in allergen_map.values():
            if allergen in dangerous_ingredients:
                dangerous_ingredients.pop(allergen)
    return allergen_map


def compute_part_two(file: Path) -> str:
    """
    Compute submission value for part two

    :param file:
    :return:
    """

    foods: list = list(load_foods(file=file))
    allergen_map = map_allergens(foods=foods)
    sorted_allergen_map = dict(
        sorted(allergen_map.items(), key=lambda i: i[1]))
    canonical_dangerous_ingredient_list = ','.join(sorted_allergen_map.keys())
    submission = canonical_dangerous_ingredient_list
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
        print(f'\tPart two, file {f}, submit: {compute_part_two(file=Path(f))}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
