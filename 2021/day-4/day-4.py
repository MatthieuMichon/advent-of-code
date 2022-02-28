#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 4
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

BINGO_GRID_SIZE = 5


def load_contents(filename: Path) -> tuple[Iterator, list]:
    """Load and convert contents from file

    :param filename: input filename
    :return: called numbers and bingo grids
    """
    lines = iter(open(filename).readlines())
    called_numbers:Iterator[int] = (int(token) for token in next(lines).split(','))
    bingo_grids = []
    bingo_grid = []
    for line in lines:
        short_line = len(line) < BINGO_GRID_SIZE
        if short_line:
            continue
        row_numbers = {int(token) for token in line.strip().split()}
        bingo_grid.append(row_numbers)
        grid_complete = len(bingo_grid) == BINGO_GRID_SIZE
        if grid_complete:
            bingo_grids.append(bingo_grid)
            bingo_grid = []
    log.debug(f'Reached end of {filename=}')
    return called_numbers, bingo_grids


# Solver Methods ---------------------------------------------------------------


def solve_part_one(contents: tuple[Iterator, list]) -> int:
    """Solve the first part of the challenge

    :param contents: called numbers and bingo grids
    :return: expected challenge answer
    """
    called_numbers, grids = contents
    processed_grids = []
    for grid in grids:
        rows = [set(row) for row in grid]
        rows.extend((set(row) for row in list(zip(*grid))))
        processed_grids.append(rows)
    unmarked_numbers:set[int] = {0}
    for called_number in called_numbers:
        for i, grid in enumerate(processed_grids):
            bingo = False
            for j, row in enumerate(grid):
                if called_number not in row:
                    continue
                processed_grids[i][j] = row - {called_number}
                if not processed_grids[i][j]:
                    processed_grids[i].pop(j)
                    bingo = True
            if bingo:
                unmarked_numbers = {n for row in processed_grids[i] for n in row}
                break
        else:
            continue
        break
    sum_unmarked_numbers = sum(unmarked_numbers)
    answer = called_number * sum_unmarked_numbers
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
    contents = load_contents(filename=args.filename)
    compute_part_one = not args.part or args.part == 1
    if compute_part_one:
        answer_part_one = solve_part_one(contents=contents)
    # compute_part_two = not args.part or 2 == args.part
    # if compute_part_two:
    #     answer = solve_part_two(diagnostic_report=contents)
    #     print(f'part two: {answer=}')
    elapsed_time = time.perf_counter() - start_time
    print(f'{answer_part_one=}')
    print(f'done in {10000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
