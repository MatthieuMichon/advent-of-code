#!/usr/bin/env python
"""
Advent of Code 2020 - Day 3: Toboggan Trajectory
"""
import argparse
import os
import sys
from collections import Counter
from pathlib import Path
from typing import List


def count_trees(file: Path) -> int:
    """
    Count number of encountered trees

    :param file: password list file
    :return: quantity of encountered trees
    """

    trees = 0
    for index, line in enumerate(open(file)):
        line = line.strip()
        if index == 0:
            line_len = len(line)
            continue
        if line[(3 * index) % line_len] == '#':
            trees += 1
    return trees


def count_trees_with_slope(file: Path, right: int, down: int) -> int:
    """
    Count number of encountered trees

    :param file: password list file
    :return: quantity of encountered trees
    """

    trees = 0
    for index, line in enumerate(open(file)):
        line = line.strip()
        if index == 0:
            line_len = len(line)
            continue
        if index % down != 0:
            continue
        if line[(right * index // down) % line_len] == '#':
            trees += 1
    return trees


def count_trees_part2(file: Path) -> int:
    """
    Count number of encountered trees

    :param file: password list file
    :return: quantity of encountered trees
    """

    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    trees = 1
    for slope in slopes:
        trees_in_slope = count_trees_with_slope(file, *slope)
        print(f'Found {trees_in_slope} for slope {slope}')
        trees *= trees_in_slope
    return trees


def filter_valid_passwords_part2(file: Path) -> List[str]:
    """
    Filter function for part 2 of the challenge

    :param file: password list file
    :return: password meeting requirements
    """

    for line in open(file):
        min_max, char, password = line.strip().split(' ')
        first_index, second_index = [int(part) - 1
                                     for part in min_max.split('-')]
        char = char[0]
        if (password[first_index] == char) ^ (password[second_index] == char):
            yield password


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('content_file', type=str)
    args = parser.parse_args()

    content_file = Path(args.content_file)
    if not os.path.isfile(content_file):
        raise FileNotFoundError(f'File {content_file} does not exists')

    print(f'Counted {count_trees(file=content_file)}')
    print(f'Counted {count_trees_part2(file=content_file)} for part 2')

    return 0


if __name__ == '__main__':
    """
    Command line entry-point
    """
    sys.exit(main())
