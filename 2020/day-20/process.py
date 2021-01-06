#!/usr/bin/env python
"""
Advent of Code 2020: Day 20
"""

import itertools
import re
import signal
import sys
from pathlib import Path
from types import FrameType
from typing import Iterator

DEBUG = False

SEPARATOR: str = ' '
RULE_NUMBER_SUFFIX = ':'

# Common -----------------------------------------------------------------------


def load_tiles(file: Path) -> Iterator[dict]:
    """
    Decode contents of the given file

    :param file: file containing the input values
    :return: tile iterator
    """

    tile = dict()
    for line in open(file):
        if 'Tile ' in line:
            tile['id'] = int(line[5:-2])
            tile['rows'] = list()
        elif len(line) > 2:
            tile['rows'].append(line.strip())
            last_row = len(tile['rows']) == len(line.strip())
            if last_row:
                yield tile
                tile = dict()


def decode(file: Path) -> any:
    l = list(load_tiles(file))
    print(len(l))

# Part One ---------------------------------------------------------------------


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    tile_map = decode(file=file)

    corners_id_product = 0
    return corners_id_product


# Part Two ---------------------------------------------------------------------


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    corners_id_product = 0
    return corners_id_product


# Main -------------------------------------------------------------------------


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    files = ['./example.txt', './input.txt']
    files = ['./example.txt']
    #files = []
    for f in files:
        print(f'In file {f}:')
        print(f'\tPart One: {process(file=Path(f))}')

    files = ['./example_part2.txt', './input.txt']
    #files = ['./input.txt']
    #files = []
    for f in files:
        print(f'In file {f}:')
        print(f'\tPart Two: {process_part2(file=Path(f))}')

    return 0


def handle_sigint(signal_value: signal.Signals, frame: FrameType) -> None:
    """
    Interrupt signal call-back method

    :param signal_value: signal (expected SIGINT)
    :param frame: current stack frame at the time of signal
    :return: nothing
    """

    assert signal_value == signal.SIGINT
    print(frame.f_locals)
    sys.exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    sys.exit(main())
