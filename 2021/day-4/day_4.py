#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 4
Puzzle Solution in Python
"""

import logging
import sys
import time
from pathlib import Path

from common.support import configure_logger, parse_arguments

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# Common Methods ---------------------------------------------------------------

BINGO_GRID_SIZE = 5


def load_contents(filename: Path) -> tuple[list, list]:
    """Load and convert contents from file

    :param filename: input filename
    :return: called numbers and bingo grids
    """
    with open(filename, encoding='utf-8') as buffer:
        lines = iter(buffer.readlines())
    called_numbers:[int] = [int(token) for token in next(lines).split(',')]
    bingo_grids = []
    bingo_grid = []
    for line in lines:
        short_line = len(line) < BINGO_GRID_SIZE
        if short_line:
            continue
        row_numbers = [int(token) for token in line.strip().split()]
        bingo_grid.append(row_numbers)
        grid_complete = len(bingo_grid) == BINGO_GRID_SIZE
        if grid_complete:
            bingo_grids.append(bingo_grid)
            bingo_grid = []
    log.debug(f'Reached end of {filename=}')
    return called_numbers, bingo_grids


# Solver Methods ---------------------------------------------------------------


def solve_part_one(contents: tuple[list, list]) -> int:
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
    called_number = 0
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


def solve_part_two(contents: tuple[list, list]) -> int:
    """Solve the second part of the challenge

    :param contents: called numbers and bingo grids
    :return: expected challenge answer
    """
    called_numbers, grids = contents
    processed_grids = {}
    for i, grid in enumerate(grids):
        rows = [set(row) for row in grid]
        rows.extend((set(row) for row in list(zip(*grid))))
        processed_grids[i] = rows
    unmarked_numbers:set[int] = {0}
    last_called_number = -1
    for called_number in called_numbers:
        for i, _ in enumerate(grids):
            if i not in processed_grids:
                continue
            for j, row in enumerate(processed_grids[i]):
                if called_number not in row:
                    continue
                processed_grids[i][j] = row - {called_number}
                if not processed_grids[i][j]:
                    processed_grids[i].pop(j)
                    unmarked_numbers = {n for row in processed_grids[i] for n in row}
                    processed_grids.pop(i)
                    last_called_number = called_number
                    break
    sum_unmarked_numbers = sum(unmarked_numbers)
    answer = last_called_number * sum_unmarked_numbers
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
    contents = load_contents(filename=args.filename)
    compute_part_one = not args.part or args.part == 1
    answer_part_one = 0
    if compute_part_one:
        answer_part_one = solve_part_one(contents=contents)
    compute_part_two = not args.part or 2 == args.part
    answer_part_two = 0
    if compute_part_two:
        answer_part_two = solve_part_two(contents=contents)
    elapsed_time = time.perf_counter() - start_time
    print(f'{answer_part_one=}')
    print(f'{answer_part_two=}')
    print(f'done in {10000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
