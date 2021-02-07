#!/usr/bin/env python

"""Advent of Code 2020

Day 24: Lobby Layout
"""

import os
import sys
from collections import Counter
from pathlib import Path


# Common -----------------------------------------------------------------------


DIRECTION_MAP = {
    'ne': '1', 'se': '3', 'sw': '4', 'nw': '6',
    'e': '2', 'w': '5',
}
ANGLES = [-30 + 60 * int(v) for v in sorted(DIRECTION_MAP.values())]


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


def optimize(paths: list[list[int]]) -> list[list[int]]:
    """Optimize a list of paths

    :param paths: paths as a list of heading in degrees
    :return: optimized paths as a list of heading in degrees
    """
    paths = [Counter(p) for p in paths]
    optimized_paths = list()
    for path in paths:
        optimized_steps = list()
        for angle in ANGLES:
            if angle > 180:
                break
            distance = path[angle] - path[180 + angle]
            heading = angle if distance >= 0 else 180 + angle
            optimized_steps.extend([heading] * abs(distance))
        optimized_paths.append(optimized_steps)
    return optimized_paths


def print_part_one(inputs: list[Path]) -> None:
    """Print answer for part one

    :param inputs: list of puzzle input files
    :return: nothing
    """
    for file in inputs:
        paths = read_paths(file=file)

    paths = optimize(paths=paths)
    len(paths)

# Common -----------------------------------------------------------------------


def main() -> int:
    """Main function

    :return: shell exit code
    """
    inputs = [
        'test.txt',
        #'example.txt',
    ]
    print_part_one(inputs=[Path(i) for i in inputs])
    return 0


if __name__ == '__main__':
    sys.exit(main())
