#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 7
Puzzle Solution in Python
"""

import logging
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from common.support import configure_logger, parse_arguments

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> [int]:
    """Load and convert contents from file

    :param filename: input filename
    :return: list of integers
    """
    with open(filename, encoding='utf-8') as buffer:
        line = next(iter(buffer.readlines()))
        tokens = [int(t) for t in line.strip().split(',')]
        return tokens


# Solver Methods ---------------------------------------------------------------


def compute_fuel_cost(h_positions: [int], h_position: int) -> int:
    """Compute fuel cost for a given configuration

    :param h_positions: list of initial horizontal positions
    :param h_position: final horizontal position
    :return: total fuel required for reaching final position
    """
    fuel = sum(abs(h_position - pos) for pos in h_positions)
    return fuel


def solve_part_one(contents: any) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    positions = sorted(set(contents))
    min_map = {compute_fuel_cost(contents, pos): pos for pos in positions}
    answer = min(min_map.keys())
    log.debug(f'Found min in listed positions: {answer}')
    return answer


def solve_part_two(contents: any) -> int:
    """Solve the second part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    ...
    answer = 0
    return answer


# Support Methods --------------------------------------------------------------


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """
    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'called with {args=}')
    start_time = time.perf_counter()
    contents = load_contents(filename=args.filename)
    compute_part_one = not args.part or args.part == 1
    answer_part_one = 0
    if compute_part_one:
        answer_part_one = solve_part_one(contents=contents)
    compute_part_two = not args.part or 2 == args.part
    answer_part_two = 0
    if compute_part_two:
        answer_part_two = solve_part_two(contents=contents)
    elapsed_time = time.perf_counter() - start_time
    print(f'{answer_part_one=}')
    print(f'{answer_part_two=}')
    print(f'done in {10000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
