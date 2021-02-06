#!/usr/bin/env python

"""Advent of Code 2020

Day 24: Lobby Layout
"""

import os
import sys
from pathlib import Path


# Common -----------------------------------------------------------------------


DIRECTION_MAP = {
    'ne': '1', 'se': '3', 'sw': '4', 'nw': '6',
    'e': '2', 'w': '5',
}


def read_paths(file: Path) -> list[list[int]]:
    """Read tile paths from a file

    :param file: file containing path directions
    :return: paths as a list of heading in degrees
    """
    paths = open(file).read()
    for d, v in DIRECTION_MAP.items():
        paths = paths.replace(d, v)
    paths = paths.split(os.linesep)
    paths = [[-30 + (int(s) * 60) for s in p] for p in paths if len(p)]
    return paths


# Part One  --------------------------------------------------------------------


def print_part_one(inputs: list[Path]) -> None:
    """Print answer for part one

    :param inputs: list of puzzle input files
    :return: nothing
    """

    for file in inputs:
        paths = read_paths(file=file)
        print(len(paths))


# Common -----------------------------------------------------------------------


def main() -> int:
    """Main function

    :return: shell exit code
    """
    inputs = [
        'example.txt',
    ]
    print_part_one(inputs=inputs)
    return 0


if __name__ == '__main__':
    sys.exit(main())
