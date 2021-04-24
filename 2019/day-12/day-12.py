#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 12
Puzzle Solution in Python
"""

import argparse
import logging
import os
import sys

from enum import Enum, IntEnum, auto
from types import SimpleNamespace as sn
from typing import Iterator

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def load_contents(filename: str) -> Iterator[map]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding a list of integers
    """
    lines = open(filename).read().strip().strip('<>').split(os.linesep)
    for line in lines:
        axis = [token.split('=') for token in line.strip('<>').split(',')]
        axis = {name: int(value) for name, value in axis}
        yield axis


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


def configure_logger(level: int):
    """Configure logging

    :param level: verbosity level
    :return: nothing
    """
    logger = logging.getLogger()
    logger.handlers = []
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(level=logging.WARNING)
    stdout.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(stdout)
    if level >= 2:
        stdout.setLevel(level=logging.DEBUG)
        logger.setLevel(level=logging.DEBUG)
    elif level >= 1:
        stdout.setLevel(level=logging.INFO)
        logger.setLevel(level=logging.INFO)


def parse_arguments() -> argparse.Namespace:
    """Parse arguments provided by the command-line

    :return: list of decoded arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    pa = parser.add_argument
    pa('filename', type=str, help='input contents filename')
    pa('-p', '--part', type=int, help='solve only the given part')
    pa('-v', '--verbose', action='count', default=0)
    arguments = parser.parse_args()
    return arguments


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """
    args = parse_arguments()
    configure_logger(level=args.verbose)
    log.info(f'Arguments: {args}')
    compute_part_one = not args.part or 1 == args.part
    compute_part_two = not args.part or 2 == args.part
    if compute_part_one:
        contents = list(load_contents(filename=args.filename))
        answer = -1
        print(f'part one: {answer=}')
    if compute_part_two:
        answer = -1
        print(f'part two: {answer=}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
