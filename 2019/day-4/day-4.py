#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day Four
Puzzle Solution in Python
"""

import argparse
import logging
import sys

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def decode(argument: str) -> tuple[list[int], ...]:
    """Decode argument string from command line

    :param argument: argument string
    :return: pair of list of digits
    """
    char_lists = map(list, argument.split('-'))
    range_ = tuple(list(map(int, clist)) for clist in char_lists)
    return range_


def count_pwd(range_: tuple[list[int], ...],
              digits: list[int], length: int) -> int:
    """Recursively count passwords with a list of prefix digits

    :param range_: min and max number
    :param digits: list of prefix digits
    :param length: expected password length
    :return: number of passwords matching requirements
    """
    digit_index = len(digits)
    decreasing_digit = digit_index >= 2 and digits[-1] < digits[-2]
    if decreasing_digit:
        return 0
    stop = digit_index == length
    if stop:
        same_adjacent_digits = len(set(digits)) < len(digits)
        return 1 if same_adjacent_digits else 0
    min_digits = range_[0][:1+digit_index]
    max_digits = range_[1][:1+digit_index]
    pwd_count = 0
    for next_digit in range(10):
        next_digits = digits.copy()
        next_digits.append(next_digit)
        if not min_digits <= next_digits <= max_digits:
            continue
        pwd_count += count_pwd(
            range_=range_, digits=next_digits, length=length)
    return pwd_count


# Solving Methods --------------------------------------------------------------


def solve(contents: tuple[list[int], ...]) -> int:
    """Solve the first part of the puzzle

    :param contents: list of offsets per wire
    :return: answer of the puzzle
    """
    length: int = len(contents[0])
    digits = list()
    pwd_count = count_pwd(range_=contents, digits=digits, length=length)
    return pwd_count


def solve_part_two(contents: tuple[list[int], ...]) -> int:
    """Solve the second part of the puzzle

    :param contents: list of offsets per wire
    :return: answer of the puzzle
    """
    answer = -1
    return answer


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
    pa('puzzle_input', type=str, help='puzzle input value')
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
        contents = decode(argument=args.puzzle_input)
        answer = solve(contents=contents)
        print(answer)
    if compute_part_two:
        contents = decode(argument=args.puzzle_input)
        answer = solve_part_two(contents=contents)
        print(answer)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
