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

    :param layout: seat layout
    :param row: row index of the seat of interest
    :param col: column index of the seat of interest
    :return: quantity of occupied seats adjacent to the seat of interest
    """

    top_row = layout[row-1][col-1:col+2]
    ctr_row = [layout[row][col-1], layout[row][col+1]]
    bot_row = layout[row+1][col-1:col+2]
    adj_seats = top_row + ctr_row + bot_row

    occupied_adjacent_seats = sum(1 for s in adj_seats if s == '#')

    return occupied_adjacent_seats


def count_occupied_seats(layout: List[List[str]]) -> int:
    """
    Count quantity of occupied seats in a given layout

    :param layout: seat layout
    :return: quantity of occupied seats
    """

    occupied_seats = sum(sum(1 for seat in r if seat == '#') for r in layout)
    return occupied_seats


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

    updated_layout = deepcopy(layout)

    occupied_layout = compute_occupied_layout(updated_layout)

    depth = len(updated_layout)
    width = len(updated_layout[0])
    for r in range(1, depth - 1):
        for c in range(1, width - 1):
            if updated_layout[r][c] != 'L':
                continue
            elif occupied_layout[r][c] == 0:
                updated_layout[r][c] = '#'

    occupied_updated_layout = compute_occupied_layout(updated_layout)

    depth = len(updated_layout)
    width = len(updated_layout[0])
    for r in range(1, depth - 1):
        for c in range(1, width - 1):
            if updated_layout[r][c] != '#':
                continue
            elif occupied_updated_layout[r][c] >= 4:
                updated_layout[r][c] = 'L'

    return updated_layout


def count_occupied_visible_seats(
        layout: List[List[str]], row=int, col=int) -> int:
    """
    Return the quantity of occupied visible seats

    :param layout: seat layout
    :param row: row index of the seat of interest
    :param col: column index of the seat of interest
    :return: quantity of occupied seats adjacent to the seat of interest
    """

    inside = lambda r_, c_: \
        (0 <= r_ < len(layout)) and (0 <= c_ < len(layout[0]))

    # right ray
    dist = 1
    path_list = {(45 * path):None for path in range(1, 9)}
    while not all(path_list.values()):

        # North
        if not path_list[360]:
            r = row - dist
            c = col
            if not inside(r, c):
                path_list[360] = 'B'  # border
            else:
                seat = layout[r][c]
                if seat in ['#',  'L']:
                    path_list[360] = seat

        # North-East
        if not path_list[45]:
            r = row - dist
            c = col + dist
            if not inside(r, c):
                path_list[45] = 'B'  # border
            else:
                seat = layout[r][c]
                if seat in ['#',  'L']:
                    path_list[45] = seat

        # East
        if not path_list[90]:
            r = row
            c = col + dist
            if not inside(r, c):
                path_list[90] = 'B'  # border
            else:
                seat = layout[r][c]
                if seat in ['#',  'L']:
                    path_list[90] = seat

        # South-East
        if not path_list[135]:
            r = row + dist
            c = col + dist
            if not inside(r, c):
                path_list[135] = 'B'  # border
            else:
                seat = layout[r][c]
                if seat in ['#',  'L']:
                    path_list[135] = seat

        # South
        if not path_list[180]:
            r = row + dist
            c = col
            if not inside(r, c):
                path_list[180] = 'B'  # border
            else:
                seat = layout[r][c]
                if seat in ['#',  'L']:
                    path_list[180] = seat

        # South-West
        if not path_list[225]:
            r = row + dist
            c = col - dist
            if not inside(r, c):
                path_list[225] = 'B'  # border
            else:
                seat = layout[r][c]
                if seat in ['#',  'L']:
                    path_list[225] = seat

        # West
        if not path_list[270]:
            r = row
            c = col - dist
            if not inside(r, c):
                path_list[270] = 'B'  # border
            else:
                seat = layout[r][c]
                if seat in ['#',  'L']:
                    path_list[270] = seat

        # North-West
        if not path_list[315]:
            r = row - dist
            c = col - dist
            if not inside(r, c):
                path_list[315] = 'B'  # border
            else:
                seat = layout[r][c]
                if seat in ['#',  'L']:
                    path_list[315] = seat

        dist += 1

    occupied_visible_seats = sum(1 for p in path_list.values() if p == '#')

    return occupied_visible_seats



def compute_visible_occupied_layout(layout: List[List[str]]) -> List[List[str]]:
    """
    Compute occupied seat map for part 2

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
                row.append(count_occupied_visible_seats(
                    layout=layout, row=r, col=c))
        row.append('.')
        occupied_layout.append(row)
    occupied_layout.append(['.'] * width)

    return occupied_layout



def compute_round_part2(layout: List[List[str]]) -> List[List[str]]:
    """
    Apply round of rules defined in part 2

    :param layout: seat layout
    :return: layout following a round
    """

    updated_layout = deepcopy(layout)

    occupied_layout = compute_visible_occupied_layout(updated_layout)

    depth = len(updated_layout)
    width = len(updated_layout[0])
    for r in range(1, depth - 1):
        for c in range(1, width - 1):
            if updated_layout[r][c] != 'L':
                continue
            elif occupied_layout[r][c] == 0:
                updated_layout[r][c] = '#'

    occupied_updated_layout = compute_visible_occupied_layout(updated_layout)

    depth = len(updated_layout)
    width = len(updated_layout[0])
    for r in range(1, depth - 1):
        for c in range(1, width - 1):
            if updated_layout[r][c] != '#':
                continue
            elif occupied_updated_layout[r][c] >= 5:
                updated_layout[r][c] = 'L'

    return updated_layout


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    rounds = 0
    updated_layout = extend(layout=[list(l.strip()) for l in open(file)])
    layout = [['-' for s in row] for row in updated_layout]
    while updated_layout != layout:
        rounds += 1
        layout = updated_layout
        updated_layout = compute_round(layout=layout)

    print(f'Converged after {rounds} rounds')
    occupied_seats = count_occupied_seats(layout=updated_layout)
    submission = occupied_seats

    return submission


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    rounds = 0
    updated_layout = extend(layout=[list(l.strip()) for l in open(file)])
    layout = [['-' for s in row] for row in updated_layout]
    while updated_layout != layout:
        rounds += 1
        layout = updated_layout
        updated_layout = compute_round_part2(layout=layout)

    print(f'Converged after {rounds} rounds')
    occupied_seats = count_occupied_seats(layout=updated_layout)
    submission = occupied_seats

    return submission


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    if False:
        layout__ = extend(layout=[list(l.strip()) for l in open('./part2_sample1.txt')])
        count_occupied_visible_seats(layout__, 5, 4)

        return 0

    for file in TXT_FILES:
        submission = process(file=Path(file))
        print(f'In file {file}, submission: {submission}')

    print('Part 2')

    for file in TXT_FILES:
        submission = process_part2(file=Path(file))
        print(f'In file {file}, submission: {submission}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
