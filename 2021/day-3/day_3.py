#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 3
Puzzle Solution in Python
"""

import logging
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Iterator

from common.support import configure_logger, parse_arguments

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> Iterator[tuple]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator
    """
    with open(filename, encoding='utf-8') as buffer:
        for line in iter(buffer.readlines()):
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


def solve_part_two(diagnostic_report: Iterator[tuple]) -> int:
    """Solve the first part of the challenge

    :param diagnostic_report: binary numbers
    :return: expected challenge answer
    """
    numbers = set(diagnostic_report)
    for bit_index, _ in enumerate(zip(*numbers)):
        bits = list(zip(*numbers))[bit_index]
        values = Counter(bits).most_common()
        if len(values) == 1:
            break
        most_common =\
            values[0][0] if values[0][1] > values[1][1] else '1'
        numbers = set(number for number in numbers if number[bit_index] == most_common)
    oxygen_generator_rating = int(''.join(numbers.pop()), 2)
    numbers = set(diagnostic_report)
    for bit_index, _ in enumerate(zip(*numbers)):
        bits = list(zip(*numbers))[bit_index]
        values = Counter(bits).most_common()
        if len(values) == 1:
            break
        least_common =\
            values[1][0] if values[0][1] > values[1][1] else '0'
        numbers = set(number for number in numbers if number[bit_index] == least_common)
    co2_scrubber_rating = int(''.join(numbers.pop()), 2)
    answer = oxygen_generator_rating * co2_scrubber_rating
    return answer


# Support Methods --------------------------------------------------------------


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
    compute_part_two = not args.part or 2 == args.part
    if compute_part_two:
        answer = solve_part_two(diagnostic_report=contents)
        print(f'part two: {answer=}')
    elapsed_time = time.perf_counter() - start_time
    print(f'done in {1000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
