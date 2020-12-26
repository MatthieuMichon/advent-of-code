#!/usr/bin/env python
"""
Advent of Code 2020: Day 13
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

    lines = (l for l in open(file))
    timestamp = int(next(lines))
    bus_id_list = [int(bus_id) for bus_id in next(lines).strip().split(',')
                   if bus_id.isdecimal()]

    time = timestamp
    while not any(time % bus_id == 0 for bus_id in bus_id_list):
        time += 1
    earliest_bus = next(bus_id for bus_id in bus_id_list if time % bus_id == 0)

    submission = (time - timestamp) * earliest_bus
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

    # print('Part 2')
    #
    # for file in TXT_FILES:
    #     submission = process_part2(file=Path(file))
    #     print(f'In file {file}, submission: {submission}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
