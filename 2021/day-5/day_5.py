#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 5
Puzzle Solution in Python
"""

import argparse
import logging
import sys
import time
from pathlib import Path

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> tuple[tuple, tuple]:
    """Load and convert contents from file

    :param filename: input filename
    :return: coordinates
    """
    with open(filename, encoding='UTF-8') as buffer:
        for line in iter(buffer.readlines()):
            tokens = line.strip().replace(',', ' ').split(' ')
            tokens.pop(2)
            integers = [int(t) for t in tokens]
            yield tuple(integers[0:2]), tuple(integers[2:4])


# Solver Methods ---------------------------------------------------------------


def solve_part_one(contents: any) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    answer = len(contents)
    return answer


def solve_part_two(contents: any) -> int:
    """Solve the second part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    answer = len(contents)
    return answer


# Support Methods --------------------------------------------------------------


def configure_logger(verbose: bool):
    """Configure logging

    :param verbose: display debug and info messages
    :return: nothing
    """
    logger = logging.getLogger()
    logger.handlers = []
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(level=logging.WARNING)
    stdout.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(stdout)
    if verbose:
        stdout.setLevel(level=logging.DEBUG)
        logger.setLevel(level=logging.DEBUG)


def parse_arguments() -> argparse.Namespace:
    """Parse arguments provided by the command-line

    :return: list of decoded arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    add = parser.add_argument
    add('filename', type=str, help='input contents filename')
    add('-p', '--part', type=int, help='solve only the given part')
    add('-v', '--verbose', action='store_true', help='print extra messages')
    arguments = parser.parse_args()
    return arguments


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """
    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'called with {args=}')
    start_time = time.perf_counter()
    contents = load_contents(filename=args.filename)
    if len(list(contents)) < 5:
        print(0)
    # compute_part_one = not args.part or args.part == 1
    # answer_part_one = 0
    # if compute_part_one:
    #     answer_part_one = solve_part_one(contents=contents)
    # compute_part_two = not args.part or 2 == args.part
    # answer_part_two = 0
    # if compute_part_two:
    #     answer_part_two = solve_part_two(contents=contents)
    elapsed_time = time.perf_counter() - start_time
    # print(f'{answer_part_one=}')
    # print(f'{answer_part_two=}')
    print(f'done in {10000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
