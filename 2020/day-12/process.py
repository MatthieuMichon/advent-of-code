#!/usr/bin/env python
"""
Advent of Code 2020: Day 12
"""

import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
import os
from typing import List
import math


TXT_FILES = [Path(f) for f in os.listdir('./') if '.txt' in f]


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    heading = 90
    east_west_pos = 0
    north_south_pos = 0

    instructions = [l.strip() for l in open(file)]
    for i in instructions:
        action = i[0]
        value = int(i[1:])
        if action == 'R':
            heading = (heading + value) % 360
        elif action == 'L':
            heading = (heading - value) % 360
        if action == 'E':
            east_west_pos += value
        if action == 'W':
            east_west_pos -= value
        if action == 'N':
            north_south_pos += value
        if action == 'S':
            north_south_pos -= value
        if action == 'F':
            east_west_pos += value * math.sin(float(heading) / 360.0 * 2.0 * math.pi)
            north_south_pos += value * math.cos(heading / 360 * 2 * math.pi)

    manhattan_distance = int(abs(east_west_pos) + abs(north_south_pos))

    return manhattan_distance


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    for file in TXT_FILES:
        submission = process(file=Path(file))
        print(f'In file {file}, submission: {submission}')

    return 0
    #
    # print('Part 2')
    #
    # for file in TXT_FILES:
    #     submission = process_part2(file=Path(file))
    #     print(f'In file {file}, submission: {submission}')
    # return 0


if __name__ == '__main__':
    sys.exit(main())
