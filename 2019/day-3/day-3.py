#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day Three
Puzzle Solution in Python
"""

import argparse
import logging
import operator
import os
import sys
from typing import Iterator

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def convert_token(token: str) -> tuple[int]:
    """Converts string token into 2d grid offset

    :param token: token in string format
    :return: 2d grid offset in integer format
    """
    direction, length = token[:1], int(token[1:])
    assert direction in ['R', 'L', 'U', 'D']
    if direction in ['R', 'U']:
        length *= -1
    offset = (length, 0) if direction in ['R', 'L'] else (0, length)
    return offset


def load_contents(filename: str) -> list[list[tuple[int]]]:
    """Load contents from the given file

    :param filename: filename as string
    :return: converted contents
    """
    wires = list(open(filename).read().strip().split(os.linesep))
    log.info(f'Loaded {len(wires)} wires from {filename}')
    assert 0 == len(wires) % 2
    contents = [[convert_token(t) for t in w.split(',')] for w in wires]
    return contents


def enumerate_corners(wire: list[tuple[int]]) -> Iterator[tuple[int]]:
    """Enumerate corners for the given wire path

    :param wire: list of segments for a given wire
    :yield: location of segment corner
    """
    corner = (0, 0)
    for offset in wire:
        corner = tuple(map(operator.add, corner, offset))
        yield corner


# Solving Methods --------------------------------------------------------------


def solve(contents: list[list[tuple[int]]]) -> int:
    """Solve the first part of the puzzle

    :param contents: list of offsets per wire
    :return: answer of the puzzle
    """
    answer = 0


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = ('%(asctime)s - %(levelname)s - %(module)s - '
              '%(funcName)s - %(message)s')


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
    compute_part_two = not args.part or 2 == args.part
    compute_part_two = False
    if compute_part_one:
        contents = load_contents(filename=args.filename)
        answer = solve(contents=contents)
        print(answer)
    if compute_part_two:
        contents = load_contents(filename=args.filename)
        #answer = solve_part_two(contents=contents)
        print(answer)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
