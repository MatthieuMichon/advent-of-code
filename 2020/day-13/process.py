#!/usr/bin/env python
"""
Advent of Code 2020: Day 13
"""

import sys
from pathlib import Path
import os


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

    lines = (l for l in open(file))
    next(lines)  # skip timestamp
    bus_id_offsets = {int(bus_id): -i
                      for i, bus_id in enumerate(next(lines).strip().split(','))
                      if bus_id.isnumeric()}
    time = 0
    global_offset = 1
    for bus_id, offset in bus_id_offsets.items():
        while (time - offset) % bus_id != 0:
            time += global_offset
        global_offset *= bus_id

    debug = False
    if debug:
        bus_id_list = list(bus_id_offsets.keys())
        for t in range(time-5, time+max(bus_id_list)):
            print(f'{t}\t{" ".join("D" if (t % b == 0) else "." for b in bus_id_list)}')

    submission = time

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

    for file in TXT_FILES:
        submission = process_part2(file=Path(file))
        print(f'In file {file}, submission: {submission}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
