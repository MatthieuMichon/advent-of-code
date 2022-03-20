#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 8
Puzzle Solution in Python
"""

import logging
import sys
import time
from pathlib import Path
from typing import Generator

from common.support import configure_logger, parse_arguments

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> Generator:
    """Load and convert contents from file

    :param filename: input filename
    :return: list of integers
    """
    with open(filename, encoding='utf-8') as buffer:
        for line in buffer.readlines():
            patterns, outputs = [part.strip().split(' ')
                                 for part in line.split('|')]
            yield patterns, outputs


# Solver Methods ---------------------------------------------------------------


def solve_part_one(contents: any) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    easy_digits = {
        1: 2,
        4: 4,
        7: 3,
        8: 7,
    }

    entries = list(zip(*contents))[1]
    easy_digit_count = 0
    for outputs in entries:
        easy_digit_count += sum(len(output) in easy_digits.values()
                                for output in outputs)
    answer = easy_digit_count
    return answer


def print_segments(segments: str) -> None:
    """Print segments according to a convention

    :param segments: string of individual segments
    :return: nothing
    """
    if 'a' in segments:
        print(' #### ')
    else:
        print(' ---- ')
    for _ in range(2):
        print(f'{"#" if "f" in segments else "-"}    '
              f'{"#" if "b" in segments else "-"}')
    if 'g' in segments:
        print(' #### ')
    else:
        print(' ---- ')
    for _ in range(2):
        print(f'{"#" if "e" in segments else "-"}    '
              f'{"#" if "c" in segments else "-"}')
    if 'd' in segments:
        print(' #### ')
    else:
        print(' ---- ')


def solve_part_two(contents: any) -> int:
    """Solve the second part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    known_segment_map = {
        2: {'upper-right', 'lower-right'},
        3: {'top', 'upper-right', 'lower-right'},
        4: {'upper-left', 'middle', 'upper-right', 'lower-right'},
    }
    answer = len(contents)
    return answer


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
    print(f'done in {1000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
