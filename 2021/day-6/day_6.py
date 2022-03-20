#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 6
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


DEFAULT_TIMER = 8
SPAWN_TIME = 7


def print_list(list_):
    """ Return str(self). """
    return ','.join([str(i) for i in list_])


def solve_part_one(contents: any) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    def update_timer(timer: int) -> int:
        if timer == 0:
            timer = SPAWN_TIME
        return timer - 1

    duration = 80
    lanternfishes = contents.copy()
    for day in range(1, duration + 1):
        respawned = sum(1 for timer in lanternfishes if timer == 0)
        lanternfishes = [update_timer(timer) for timer in lanternfishes]
        lanternfishes.extend([DEFAULT_TIMER] * respawned)
        log.debug(f'After {day: 2} days: {len(lanternfishes)} lanternfishes')
    answer = len(lanternfishes)
    return answer


def solve_part_two(contents: any) -> int:
    """Solve the second part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    duration = 256
    lanternfishes = defaultdict(int)
    lanternfishes.update(dict(Counter(contents)))
    for _ in range(1, 1 + duration):
        for timer in range(-1, 8):
            lanternfishes[timer] = lanternfishes[timer + 1]
        lanternfishes[6] += lanternfishes[-1]
        lanternfishes[8] = lanternfishes[-1]
    lanternfishes[-1] = 0
    answer = sum(lanternfishes.values())
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
