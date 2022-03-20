#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 1
Puzzle Solution in Python
"""

import logging
import os
import sys
import time
from pathlib import Path
from typing import Iterator

from common.support import configure_logger, parse_arguments

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> Iterator[int]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding integers
    """
    with open(filename, encoding='utf-8') as buffer:
        for line in iter(buffer.read().strip().split(os.linesep)):
            yield int(line)
    log.debug(f'Reached end of {filename=}')


# Solver Methods ---------------------------------------------------------------


def solve_part_one(depths: [int]) -> int:
    """Solve the first part of the challenge

    :param depths: list of depth values
    :return: expected challenge answer
    """
    pairs = zip(depths[:-1], depths[1:])
    answer = sum(a < b for a, b in pairs)
    return answer


def solve_part_two(depths: [int]) -> int:
    """Solve the second part of the challenge

    :param depths: list of depth values
    :return: expected challenge answer
    """
    baseline = zip(depths[:-3], depths[1:-2], depths[2:-1])
    baseline_sums = (sum(i) for i in baseline)
    sample = zip(depths[1:-2], depths[2:-1], depths[3:])
    sample_sums = (sum(i) for i in sample)
    pairs = zip(baseline_sums, sample_sums)
    answer = sum(a < b for a, b in pairs)
    return answer


# Support Methods --------------------------------------------------------------


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """
    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'Arguments: {args}')
    start_time = time.perf_counter()
    contents = list(load_contents(filename=args.filename))
    compute_part_one = not args.part or args.part == 1
    if compute_part_one:
        answer = solve_part_one(depths=contents)
        print(f'part one: {answer=}')
    compute_part_two = not args.part or 2 == args.part
    if compute_part_two:
        answer = solve_part_two(depths=contents)
        print(f'part two: {answer=}')
    elapsed_time = time.perf_counter() - start_time
    print(f'done in {10000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
