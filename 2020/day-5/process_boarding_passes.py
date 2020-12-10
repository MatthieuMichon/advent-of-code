#!/usr/bin/env python
"""
Advent of Code 2020 - Day 4: Passport Processing
"""
import sys
from pathlib import Path
import bisect

from typing import Iterator, Mapping


INPUT_FILES = ['./short-input.txt', './input.txt']
REQUIRED_FIELDS = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    # 'cid',
]


def process_boarding_passes(file: Path, verbose: bool) -> int:
    """
    Process a given boarding pass file

    :param file: boarding pass file to process
    :return: highest id of all the boarding passes
    """

    highest_id = 0
    for seat in open(file):
        seat = seat.strip().replace('F', '0').replace('B', '1')
        seat = seat.replace('L', '0').replace('R', '1')
        id_ = int(seat, 2)
        if verbose:
            print(f'seat {seat}, id {id_}')
        highest_id = id_ if id_ > highest_id else highest_id
    return highest_id


def process_boarding_passes_part2(file: Path) -> int:
    """
    Process a given boarding pass file

    :param file: boarding pass file to process
    :return: highest id of all the boarding passes
    """

    id_list = list()
    for seat in open(file):
        seat = seat.strip().replace('F', '0').replace('B', '1')
        seat = seat.replace('L', '0').replace('R', '1')
        id_ = int(seat, 2)
        bisect.insort(id_list, id_)

    seat_id = 0
    for i, id_ in enumerate(id_list):
        if 0 < i < len(id_list):
            if id_list[i - 1] + 1 != id_:
                seat_id = id_list[i - 1] + 1
                break

    return seat_id


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    for file in INPUT_FILES:
        verbose = 'short' in file
        highest_id = process_boarding_passes(
            file=Path(file), verbose=verbose)
        print(f'In file {file}, highest ID: {highest_id}')

    print('Part 2')

    seat_id = process_boarding_passes_part2(file=Path('./input.txt'))
    print(f'Seat ID: {seat_id}')

    return 0


if __name__ == '__main__':
    """
    Command line entry-point
    """
    sys.exit(main())
