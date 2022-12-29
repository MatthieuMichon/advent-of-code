#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 11
Puzzle Solution in Python
"""

import copy
import logging
import sys
import time
from collections import namedtuple

from pathlib import Path
from typing import Iterator

from common.support import parse_arguments, configure_logger
from itertools import product

log = logging.getLogger(__name__)

DEFAULT_FILE = 'example-input.txt'
DEFAULT_FILE = 'input.txt'
EXIT_SUCCESS = 0

Position = namedtuple('Position', ['col', 'row'])


def load_contents(filename: Path) -> dict[Position: int]:
    """Load and convert contents from file

    :param filename: input filename
    :return: contents structured as a map
    """

    with open(filename, encoding='utf-8') as buffer:
        contents = {Position(col, row):
                        {"energy": int(level), "flashes": 0, "flashed": False}
                    for row, line in enumerate(buffer.readlines())
                    for col, level in enumerate(line.strip())}
        return contents


AXIS = 2
STENCILS = tuple(c for c in product((-1, 0, 1), repeat=AXIS) if any(c))


def compute_neighbors(pos: tuple[int]) -> tuple:
    """Compute neighbors

    :param pos: point coordinates
    :return: list of neighbors
    """
    neighbors = tuple(tuple([sum(x) for x in zip(pos, s)]) for s in STENCILS)
    return neighbors


def solve_first_part(contents: any) -> int:
    """Solve the first part of the challenge

    :param contents: decoded contents
    :return: answer for the first part
    """

    THRESHOLD = 9

    def step(octopuses_: dict) -> dict:
        # increment energy level of all octopuses_
        for pos in octopuses_:
            octopuses_[pos]['energy'] += 1
            octopuses_[pos]['flashed'] = False
        while any(v['energy'] > THRESHOLD for v in octopuses_.values()):
            # propagate flushing to neighbors
            for pos in octopuses_:
                flushing = octopuses_[pos]['energy'] > THRESHOLD and not octopuses_[pos]['flashed']
                if not flushing:
                    continue
                for n in compute_neighbors(pos=pos):
                    if n in octopuses_:
                        if not octopuses_[n]['flashed']:
                            octopuses_[n]['energy'] += 1
                octopuses_[pos]['energy'] = 0
                octopuses_[pos]['flashes'] += 1
                octopuses_[pos]['flashed'] = True
        return octopuses_

    octopuses = contents
    STEPS = 100
    for i in range(STEPS):
        octopuses = step(octopuses_=octopuses)
    answer = sum(v['flashes'] for v in octopuses.values())
    return answer


def dump_octopuses_levels(octopuses: dict) -> None:
    row = 0
    while any(row in p for p in octopuses):
        col = 0
        while any(col in p for p in octopuses):
            energy = octopuses[Position(col=col, row=row)]['energy']
            print(energy if energy < 10 else '#', end='')
            col += 1
        print('')
        row += 1


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """

    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'called with {args=}')

    start_time = time.perf_counter()

    contents = load_contents(filename=args.filename)
    compute_first_part = \
        'solve_first_part' in globals() and (not args.part or args.part == 1)
    compute_second_part = \
        'solve_second_part' in globals() and (not args.part or args.part == 2)
    answer_part_one = \
        solve_first_part(contents=contents) if compute_first_part else 0
    answer_part_two = \
        solve_second_part(contents=contents) if compute_second_part else 0

    elapsed_time = time.perf_counter() - start_time

    print(f'{answer_part_one=}')
    print(f'{answer_part_two=}')
    print(f'done in {1000 * elapsed_time:0.1f} milliseconds')

    return EXIT_SUCCESS


if __name__ == '__main__':
    """Standalone entry-point"""
    NO_INPUT_FILE = 1 == len(sys.argv)
    if NO_INPUT_FILE:
        default_input = Path(__file__).parent / DEFAULT_FILE
        sys.argv.append(str(default_input))
    sys.exit(main())
