#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 6
Puzzle Solution in Python
"""

import logging
import sys
import time
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

SPAWN_TIME = 7
DURATION = 256


def print_list(list_): # real signature unknown
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

    lanternfishs = contents.copy()
    for _ in range(1, DURATION + 1):
        print(_)
        respawned = sum(1 for timer in lanternfishs if timer == 0)
        lanternfishs = [update_timer(timer) for timer in lanternfishs]
        lanternfishs.extend([8] * respawned)
        answer = len(lanternfishs)
    return answer


def count_directly_spawned_lanternfishs(days: int, initial_timer: int) -> int:
    total_days = days + (7 - initial_timer)
    return total_days // 7


def solve_part_two(contents: any) -> int:
    """Solve the second part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    def update_timer(timer: int) -> int:
        if timer == 0:
            timer = SPAWN_TIME
        return timer - 1

    def list_children(timer: int, duration: int) -> any:
        for cycle in range(duration % SPAWN_TIME):
            yield (SPAWN_TIME - timer) + cycle * SPAWN_TIME

    # lanternfishs = [(0, v) for contents.copy()]
    for _ in range(1, 256 + 1):
        print(_)
        respawned = sum(1 for timer in lanternfishs if timer == 0)
        lanternfishs = [update_timer(timer) for timer in lanternfishs]
        lanternfishs.extend([8] * respawned)
    answer = len(lanternfishs)
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
