#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 2
Puzzle Solution in Python
"""

import argparse
import logging
import os
import sys
import time
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
        items = line.split()
        yield items[0], int(items[1])
    log.debug(f'Reached end of {filename=}')


# Solver Methods ---------------------------------------------------------------


def solve_part_one(commands: Iterator[tuple]) -> int:
    """Solve the first part of the challenge

    :param commands: list of commands
    :return: expected challenge answer
    """
    forward_pos = 0
    depth = 0
    for command in commands:
        if command[0] == 'forward':
            forward_pos += command[1]
        elif command[0] == 'down':
            depth += command[1]
        elif command[0] == 'up':
            depth -= command[1]
    answer = forward_pos * depth
    return answer


def solve_part_two(commands: Iterator[tuple]) -> int:
    """Solve the second part of the challenge

    :param commands: list of commands
    :return: expected challenge answer
    """
    forward_pos = 0
    depth = 0
    aim = 0
    for command in commands:
        if command[0] == 'forward':
            forward_pos += command[1]
            depth += aim * command[1]
        elif command[0] == 'down':
            aim += command[1]
        elif command[0] == 'up':
            aim -= command[1]
    answer = forward_pos * depth
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
        answer = solve_part_one(commands=contents)
        print(f'part one: {answer=}')
    compute_part_two = not args.part or 2 == args.part
    if compute_part_two:
        answer = solve_part_two(commands=contents)
        print(f'part two: {answer=}')
    elapsed_time = time.perf_counter() - start_time
    print(f'done in {10000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
