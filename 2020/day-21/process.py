import os
import sys
from pathlib import Path
from typing import Iterator


# Common -----------------------------------------------------------------------


def load_food_list(file: Path) -> Iterator[dict[str, list]]:
    """
    Read food lists from the given file

    :param file: file containing list of ingredients and allergens
    :return: iterator of dict objects
    """

    for line in open(file):
        line_has_contents = len(line) > len(os.linesep)
        if line_has_contents:
            line: str = line.strip()[:-1]
            lhs, rhs = line.split(' (contains ')
            ingredients: list = lhs.split(' ')
            allergens: list = rhs.split(' ')
            yield {
                'ingredients': ingredients,
                'some_allergens': allergens,
            }


def compute_part_one(file: Path) -> int:
    """
    Compute submission value for part one

    :param file:
    :return:
    """

    food_list: list[dict[str, list]] = list(load_food_list(file=file))
    dummy = -1
    return dummy


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
