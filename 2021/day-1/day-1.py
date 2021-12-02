#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 1
Puzzle Solution in Python
"""

import argparse
import logging
import os
import sys

from enum import IntEnum
from types import SimpleNamespace as sn
from typing import Iterator
from pathlib import Path

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'

# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> Iterator[int]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding integers
    """
    lines = iter(open(filename).read().strip().split(os.linesep))
    for line in lines:
        yield int(line)
    log.debug(f'Reached end of {filename=}')

# Solver Methods ---------------------------------------------------------------


def solve_part_one(depths: [int]) -> int:
    """Solve the first part of the challenge

    :param depths: list of depth values
    :return: expected challenge answer
    """
    answer = 0
    for i, depth in enumerate(depths):
        first_depth = i == 0
        prev_depth = depths[0] if first_depth else depths[i-1]
        answer += 1 if depth > prev_depth else 0
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
    log.debug(f'Arguments: {args}')
    compute_part_one = not args.part or 1 == args.part
    # compute_part_two = not args.part or 2 == args.part
    if compute_part_one:
        contents = list(load_contents(filename=args.filename))
        answer = solve_part_one(depths=contents)
        print(f'part one: {answer=}')
    # if compute_part_two:
    #     contents = next(load_contents(filename=args.filename))
    #     answer = 0
    #     print(f'part two: {answer=}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
