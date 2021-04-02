#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 10
Puzzle Solution in Python
"""

import argparse
import logging
import os
import sys
import fractions

from typing import Iterator

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


EXPECTED_CELL_CHARS = {'#', '.'}


def load_contents(filename: str) -> Iterator[set]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding maps of boolean per coordinates
    """
    lines = open(filename).read().strip().split(os.linesep)
    positions = set()
    y = 0
    for line in lines:
        if not len(line):
            log.debug(f'{filename=}, map of {len(positions)} items')
            yield positions
            positions = set()
            y = 0
            continue
        positions.update({(x, y) for x, c in enumerate(line) if c == '#'})
        y += 1
    log.debug(f'{filename=}, map of {len(positions)} items')
    yield positions


# Solver Methods ---------------------------------------------------------------


def count_asteroids(rel_positions: set) -> int:
    """Count asteroids seen given their relative positions

    :param rel_positions: set of relative positions
    :return: quantity of asteroids detected
    """
    horizontal_asteroids = set()
    upper_asteroids = set()
    lower_asteroids = set()
    for pos in rel_positions:
        zero_denominator = pos[1] == 0
        if zero_denominator:
            horizontal_asteroids.add(
                fractions.Fraction(pos[0], abs(pos[0])).as_integer_ratio())
            continue
        upper = pos[1] > 0
        if upper:
            upper_asteroids.add(
                fractions.Fraction(pos[0], pos[1]).as_integer_ratio())
            continue
        lower = pos[1] < 0
        if lower:
            lower_asteroids.add(
                fractions.Fraction(pos[0], pos[1]).as_integer_ratio())
            continue
    asteroids = len(horizontal_asteroids) \
                + len(upper_asteroids) + len(lower_asteroids)
    return asteroids


def solve(contents: set) -> int:
    """Solve puzzle part one

    :param contents: puzzle input contents
    :return: puzzle answer
    """
    detected_asteroids_map = dict()
    for asteroid in contents:
        others = contents - {asteroid}
        others = {tuple(a - b for a, b in zip(asteroid, o)) for o in others}
        detected_asteroids_map[asteroid] = count_asteroids(rel_positions=others)
    answer = max(detected_asteroids_map.values())
    return answer


def solve_part_two(contents: map) -> int:
    """Solve puzzle part two

    :param contents: puzzle input contents
    :return: puzzle answer
    """
    answer = -1
    return answer


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-12s - %(levelname)-8s - %(message)s'


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
        for map_ in load_contents(filename=args.filename):
            answer = solve(contents=map_)
            print(f'part one: answer: {answer}')
    if compute_part_two:
        for map_ in load_contents(filename=args.filename):
            answer = solve_part_two(contents=map_)
            print(f'part two: answer: {answer}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
