#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 3
Puzzle Solution in Python
"""

import argparse
import logging
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Iterator

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> Iterator[tuple]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator
    """
    for line in open(filename).readlines():
        yield tuple(line.strip())
    log.debug(f'Reached end of {filename=}')


# Solver Methods ---------------------------------------------------------------


def solve_part_one(diagnostic_report: Iterator[tuple]) -> int:
    """Solve the first part of the challenge

    :param diagnostic_report: binary numbers
    :return: expected challenge answer
    """
    diagnostic_report = tuple(zip(*diagnostic_report))
    gamma_rate = ''
    epsilon_rate = ''
    for bits in diagnostic_report:
        values = Counter(bits)
        gamma_rate += str(values.most_common()[0][0])
        epsilon_rate += str(values.most_common()[1][0])
    gamma_rate = int(gamma_rate, 2)
    epsilon_rate = int(epsilon_rate, 2)
    answer = gamma_rate * epsilon_rate
    return answer


def solve_part_two(commands: Iterator[tuple]) -> int:
    """Solve the second part of the challenge

    :param commands: list of commands
    :return: expected challenge answer
    """
    answer = 0
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
    pa = parser.add_argument
    pa('filename', type=str, help='input contents filename')
    pa('-p', '--part', type=int, help='solve only the given part')
    pa('-v', '--verbose', action='store_true', help='print extra messages')
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
    contents = list(load_contents(filename=args.filename))
    compute_part_one = not args.part or args.part == 1
    if compute_part_one:
        answer = solve_part_one(diagnostic_report=contents)
        print(f'part one: {answer=}')
    # compute_part_two = not args.part or 2 == args.part
    # if compute_part_two:
    #     answer = solve_part_two(commands=contents)
    #     print(f'part two: {answer=}')
    elapsed_time = time.perf_counter() - start_time
    print(f'done in {10000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
