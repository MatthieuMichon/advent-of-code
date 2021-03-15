#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 8
Puzzle Solution in Python
"""

import argparse
import json
import logging
import sys

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def load_contents(filename: str) -> map:
    """Load and convert contents from file

    :param filename: input filename
    :return: contents map
    """
    contents = json.load(fp=open(filename))
    return contents


# Puzzle Solving Methods -------------------------------------------------------


def solve(contents: list[int]) -> int:
    """Solve part one of the puzzle

    :param contents: decoded puzzle contents
    :return: answer for the part one of the puzzle
    """
    answer = -1
    return answer


def solve_part_two(contents: list[int]) -> int:
    """Solve part two of the puzzle

    :param contents: decoded puzzle contents
    :return: answer for the part two of the puzzle
    """
    answer = -1
    return answer


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-32s - %(levelname)-8s - %(message)s'


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
    if compute_part_one:
        contents = load_contents(filename=args.filename)
        answer = solve(contents=contents)
        print(f'part one: answer: {answer}')
    if compute_part_two:
        contents = load_contents(filename=args.filename)
        answer = solve(contents=contents)
        print(f'part two: answer: {answer}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
