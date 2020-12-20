#!/usr/bin/env python
"""
Advent of Code 2020: Day 11
"""

import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
import os
from typing import List


TXT_FILES = [Path(f) for f in os.listdir('./') if '.txt' in f]


def extend(layout: List[List[str]]) -> List[List[str]]:
    """
    Extend layout by adding a border of empty seats

    :param layout: initial layout
    :return: layout with a border of empty seats
    """

    empty_row = ['.'] * (2 + len(layout[0]))
    retval = list()
    retval.append(empty_row)
    for r in layout:
        r.insert(0, '.')
        r.insert(len(r), '.')
        retval.append(r)
    retval.append(empty_row)

    return retval


def count_occupied_adjacent_seats(
        layout: List[List[str]], row=int, col=int) -> int:
    """
    Return the quantity of occupied adjacent seats

    :param layout:
    :param row:
    :param col:
    :return:
    """

    top_row = layout[row-1][col-1:col+2]
    ctr_row = [layout[row][col-1], layout[row][col+1]]
    bot_row = layout[row+1][col-1:col+2]
    adj_seats = top_row + ctr_row + bot_row

    occupied_adjacent_seats = sum(1 for s in adj_seats if s == '#')

    return occupied_adjacent_seats


def compute_occupied_layout(layout: List[List[str]]) -> List[List[str]]:
    """
    Compute ouccpied seat map

    :param layout: seat layout
    :return: layout with number of occupied adjacent seats or '.'
    """

    depth = len(layout)
    width = len(layout[0])
    occupied_layout = list()
    occupied_layout.append(['.'] * width)
    for r in range(1, depth - 1):
        row = ['.']
        for c in range(1, width - 1):
            if layout[r][c] == '.':
                row.append('.')
            else:
                row.append(count_occupied_adjacent_seats(
                    layout=layout, row=r, col=c))
        row.append('.')
        occupied_layout.append(row)
    occupied_layout.append(['.'] * width)

    return occupied_layout


def compute_round(layout: List[List[str]]) -> List[List[str]]:
    """
    Apply round of rules defined in part 1

    :param layout: seat layout
    :return: layout following a round
    """

    occupied_layout = compute_occupied_layout(layout)

    depth = len(layout)
    width = len(layout[0])
    for r in range(1, depth - 1):
        for c in range(1, width - 1):
            if layout[r][c] != 'L':
                continue
            elif occupied_layout[r][c] == 0:
                layout[r][c] = '#'

    occupied_layout = compute_occupied_layout(layout)

    depth = len(layout)
    width = len(layout[0])
    for r in range(1, depth - 1):
        for c in range(1, width - 1):
            if layout[r][c] != '#':
                continue
            elif occupied_layout[r][c] >= 4:
                layout[r][c] = 'L'

    return layout


def compare(layout1: List[List[str]], layout2: List[List[str]]) -> bool:
    """
    Compare layouts

    :param layout1:
    :param layout2:
    :return: True if both layouts are identical
    """

    return True


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    layout = extend(layout=[list(l.strip()) for l in open(file)])
    rounds = 0
    updated_layout = [['-' for s in row] for row in layout]
    while updated_layout != layout:
        round += 1
        layout = updated_layout
        updated_layout = compute_round(layout=layout)

    submission = 0
    return submission


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    submission = 0
    return submission


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    for file in TXT_FILES:
        submission = process(file=Path(file))
        print(f'In file {file}, submission: {submission}')

    print('Part 2')

    for file in INPUT_FILES:
        submission = process_part2(file=Path(file))
        print(f'In file {file}, submission: {submission}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
