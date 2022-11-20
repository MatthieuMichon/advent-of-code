#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 9
Puzzle Solution in Python
"""

import logging
import os
import sys
import time
from pathlib import Path
from typing import Generator
from itertools import chain, groupby
from operator import itemgetter

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
        for i, line in enumerate(buffer.readlines()):
            for j, val in enumerate(line.strip()):
                yield (i, j), val

# Solver Methods ---------------------------------------------------------------


def test_low_point(contents: dict, position: tuple) -> bool:
    value = contents[position]
    north = (position[0] - 1, position[1])
    east = (position[0], position[1] + 1)
    south = (position[0] + 1, position[1])
    west = (position[0], position[1] - 1)
    if north in contents:
        north_value = contents[north]
        if north_value <= value:
            return False
    if east in contents:
        east_value = contents[east]
        if east_value <= value:
            return False
    if south in contents:
        south_value = contents[south]
        if south_value <= value:
            return False
    if west in contents:
        west_value = contents[west]
        if west_value <= value:
            return False
    return True


def solve_part_one(contents: dict) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    low_points = []
    rows = 1 + max(k[0] for k in contents.keys())
    cols = 1 + max(k[1] for k in contents.keys())
    for i in range(rows):
        for j in range(cols):
            pos = (i, j)
            if test_low_point(contents=contents, position=pos):
                low_points.append((pos, contents[pos]))
    answer = sum(1 + int(lpt[1]) for lpt in low_points)
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
    compute_part_one = not args.part or args.part == 1
    answer_part_one = 0
    if compute_part_one:
        answer_part_one = solve_part_one(contents=contents)
    # compute_part_two = not args.part or 2 == args.part
    # answer_part_two = 0
    # if compute_part_two:
    #     answer_part_two = solve_part_two(contents=contents)

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
