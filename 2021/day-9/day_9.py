#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 9
Puzzle Solution in Python
"""

import collections
import logging
import math
import sys
import time
from itertools import product
from pathlib import Path
from typing import Generator

from common.support import configure_logger, parse_arguments

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0


# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> Generator:
    """Load and convert contents from file

    :param filename: input filename
    :return: map generator
    """
    with open(filename, encoding='utf-8') as buffer:
        for row, line in enumerate(buffer.readlines()):
            for col, cell in enumerate(line.strip()):
                yield (col, row), {'height': int(cell)}


# Solver Methods ---------------------------------------------------------------


AXIS = 2
STENCILS = tuple(product((-1, 0, 1), repeat=AXIS))
STENCILS_NO_DIAG = tuple(n for n in STENCILS if 0 < sum(map(abs, n)) < 2)


def compute_neighbors(pos: tuple[int]) -> tuple:
    """Compute neighbors

    :param pos: point coordinates
    :return: list of neighbors
    """
    neighbors = tuple(tuple([sum(x) for x in zip(pos, s)]) for s in STENCILS_NO_DIAG)
    return neighbors


DEFAULT_HEIGHT = 9
DEFAULT_POS = {'height': DEFAULT_HEIGHT, 'low_point': False, 'basin': False}


def test_low_point(contents: dict, position: tuple, size: int) -> bool:
    """Check if a given position is at a lowest point

    :param contents: grid
    :param position: point coordinates
    :param size: size of the grid
    :return:
    """
    if position not in contents:
        return False
    neighbors = compute_neighbors(pos=position)
    low_point = all(
        n not in contents or
        contents[position]['height'] < contents[n]['height']
        for n in neighbors)
    return low_point


def test_basin(contents: dict, position: tuple, size: int) -> bool:
    if position not in contents or contents[position]['height'] == 9:
        return False
    neighbors = compute_neighbors(pos=position)
    basin = all(
        contents[n]['low_point'] or
        contents[n]['basin'] or
        contents[position]['height'] <= contents[n]['height']
        for n in neighbors if n in contents)
    return basin


def inside(pos, heightmap, size):
    """returns true for unfilled points
    that, by their color, would be inside the filled area
    """
    out_of_bounds = pos not in heightmap
    filled = heightmap[pos]['basin'] if not out_of_bounds else False
    basin = test_basin(contents=heightmap, position=pos, size=size) if not out_of_bounds else False
    inside_ = not out_of_bounds and not filled and basin
    return inside_


def fill(pos, heightmap, size) -> int:
    """Perform flood fill

    :param pos: fill seed coordinates
    :param heightmap: grid
    :param size: size of the grid
    :return: size of the flooded basin
    """
    basin_size = 0
    locations = collections.deque()
    locations.append(pos)
    while locations:
        pos = locations.popleft()
        if inside(pos=pos, heightmap=heightmap, size=size):
            heightmap[pos]['basin'] = True
            basin_size += 1
        for n in compute_neighbors(pos):
            if n in heightmap and inside(pos=n, heightmap=heightmap, size=size):
                locations.append(n)

    return basin_size


def display(heightmap) -> None:
    rows = 1 + max(k[0] for k in heightmap.keys())
    cols = 1 + max(k[1] for k in heightmap.keys())
    for i in range(rows):
        print(''.join([str(heightmap[(j, i)]['height']) for j in range(cols)]))
    print('')
    for i in range(rows):
        print(''.join(['#' if heightmap[(j, i)]['basin'] else '-' for j in range(cols) ]))


def solve_part_one(contents: dict) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: challenge answer
    """
    keys = contents.keys()
    rows = 1 + max(k[0] for k in keys)
    heights = (contents[pos]['height']
               for pos in keys
               if test_low_point(contents=contents, position=pos, size=rows))
    answer = sum(1 + int(h) for h in heights)
    return answer


def solve_part_two(contents: dict) -> int:
    """Solve the second part of the challenge

    :param contents: input puzzle contents
    :return: challenge answer
    """
    keys = contents.keys()
    rows = 1 + max(k[0] for k in keys)
    heightmap = {k: dict(DEFAULT_POS, **v) for k, v in contents.items()}

    low_points = (pos for pos in keys if test_low_point(contents=contents, position=pos, size=rows))
    basin_sizes = list()
    for pt in low_points:
        heightmap[pt]['low_point'] = True
        basin_sizes.append(fill(pt, heightmap=heightmap, size=rows))
        basin_sizes.sort(reverse=True)
    answer = math.prod(basin_sizes[:3])
    return answer


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """

    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'called with {args=}')

    start_time = time.perf_counter()

    contents = dict(load_contents(filename=args.filename))
    answer_part_one = solve_part_one(contents=contents) if 'solve_part_one' in globals() else 0
    answer_part_two = solve_part_two(contents=contents) if 'solve_part_two' in globals() else 0

    elapsed_time = time.perf_counter() - start_time

    print(f'{answer_part_one=}')
    print(f'{answer_part_two=}')
    print(f'done in {1000 * elapsed_time:0.1f} milliseconds')

    return EXIT_SUCCESS


if __name__ == '__main__':
    if 1 == len(sys.argv):
        script_dir = Path(__file__).parent
        sys.argv.append(str(script_dir / 'input.txt'))
    sys.exit(main())
