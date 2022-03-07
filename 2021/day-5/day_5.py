#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 5
Puzzle Solution in Python
"""

from collections import defaultdict, Counter
import logging
import sys
import time
from pathlib import Path

from common.support import configure_logger, parse_arguments

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> tuple[tuple, tuple]:
    """Load and convert contents from file

    :param filename: input filename
    :return: coordinates
    """
    with open(filename, encoding='UTF-8') as buffer:
        for line in iter(buffer.readlines()):
            tokens = line.strip().replace(',', ' ').split(' ')
            tokens.pop(2)
            integers = [int(t) for t in tokens]
            yield tuple(integers[0:2]), tuple(integers[2:4])


# Solver Methods ---------------------------------------------------------------


def draw_diagram(coordinates: dict) -> None:
    """Draw diagram of each coordinates

    :param coordinates: map of points
    :return: nothing
    """
    points = coordinates.keys()
    end_col = max(col for col, row in points)
    end_row = max(row for col, row in points)
    for row in range(0, 1 + end_row):
        line = ''
        for col in range(0, 1 + end_col):
            if (col, row) not in points:
                line += '.'
            else:
                line += str(coordinates[(col, row)])
        print(line)


def solve_part_one(contents: any) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    coordinates = defaultdict(int)
    for segment in contents:
        horizontal_segment = segment[0][0] == segment[1][0]
        vertical_segment = not horizontal_segment and segment[0][1] == segment[1][1]
        if horizontal_segment:
            start_col = min(segment[0][1], segment[1][1])
            end_col = max(segment[0][1], segment[1][1])
            x_1 = segment[0][0]
            for col in range(start_col, 1 + end_col):
                coordinates[(x_1, col)] += 1
        elif vertical_segment:
            start_row = min(segment[0][0], segment[1][0])
            end_row = max(segment[0][0], segment[1][0])
            y_1 = segment[0][1]
            for row in range(start_row, 1 + end_row):
                coordinates[(row, y_1)] += 1
    #draw_diagram(coordinates=coordinates)
    overlaps = Counter(coordinates)
    answer = sum(1 for i in list(overlaps.values()) if i >= 2)
    return answer


def solve_part_two(contents: any) -> int:
    """Solve the second part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    coordinates = defaultdict(int)
    for segment in contents:
        (x_1, y_1), (x_2, y_2) = segment
        if x_1 == x_2:
            for col in range(min(y_1, y_2), 1 + max(y_1, y_2)):
                coordinates[(x_1, col)] += 1
        elif y_1 == y_2:
            for row in range(min(x_1, x_2), 1 + max(x_1, x_2)):
                coordinates[(row, y_1)] += 1
        else: # diagonal segment
            inc_col = 1 if x_2 > x_1 else -1
            inc_row = 1 if y_2 > y_1 else -1
            for i in range(abs(x_2 - x_1) + 1):
                coordinates[(x_1 + inc_col * i, y_1 + inc_row * i)] += 1
    #draw_diagram(coordinates=coordinates)
    answer = sum(1 for i in list(Counter(coordinates).values()) if i >= 2)
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
