#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 6
Puzzle Solution in Python
"""

import argparse
import logging
import os
import sys
from functools import reduce

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


COM = 'COM'


def load_contents(filename: str) -> list[tuple]:
    """Load and convert contents from file

    :param filename: input filename
    :return: list of string tuples
    """
    lines = open(filename).read().strip().split(os.linesep)
    contents = [tuple(l.split(')')) for l in lines]
    log.info(f'Loaded {len(contents)} values from {filename}')
    return contents


def expand_orbited_objects(orbiters: dict[str], orbiter: str) -> list[str]:
    orbited_objects = list()
    orbited = orbiters[orbiter]
    orbited_objects.append(orbited)
    if COM != orbited:
        orbited_objects.extend(expand_orbited_objects(orbiters, orbited))
    return orbited_objects


# Puzzle Solving Methods -------------------------------------------------------


def solve(contents: list[tuple]) -> int:
    """Solve part one of the puzzle

    :param contents: list of integers
    :return: answer for the part one of the puzzle
    """
    orbiters = dict()
    for orbited, orbiter in contents:
        orbiters[orbiter] = orbited
    orbited_objects = dict()
    for orbiter in orbiters:
        orbited_objects[orbiter] = expand_orbited_objects(
            orbiters=orbiters, orbiter=orbiter)
    answer = sum(len(v) for v in orbited_objects.values())
    return answer


def solve_part_two(contents: list[tuple]) -> int:
    """Solve part two of the puzzle

    :param contents: list of integers
    :return: answer for the part one of the puzzle
    """
    output = -1
    return output


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = ('%(asctime)s - %(levelname)s - %(message)s')


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
        print(answer)
    if compute_part_two:
        contents = load_contents(filename=args.filename)
        answer = solve_part_two(contents=contents)
        print(answer)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
