#!/usr/bin/env python
"""
Advent of Code 2020: Day 10
"""

import sys
from collections import Counter
from pathlib import Path
from typing import List

INPUT_FILES = ['./short-input.txt', './mid-input.txt', './input.txt']


def list_joltages(file: Path) -> List[int]:
    """
    List joltages from the given file

    :param file: file containing the input values
    :return: list of joltage steps
    """

    adapter_output_joltages = sorted([int(v) for v in open(file)])
    device_input_joltage = 3 + max(adapter_output_joltages)
    joltages = [0] + adapter_output_joltages + [device_input_joltage]

    return joltages


def list_joltage_steps(file: Path) -> List[int]:
    """
    List joltages from the given file

    :param file: file containing the input values
    :return: list of joltage steps
    """

    adapter_output_joltages = sorted([int(v) for v in open(file)])
    device_input_joltage = 3 + max(adapter_output_joltages)
    joltages = [0] + adapter_output_joltages + [device_input_joltage]
    pairs = list(zip(joltages[:-1], joltages[1:]))
    joltage_steps = [p[1] - p[0] for p in pairs]

    return joltage_steps


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    joltage_steps = list_joltage_steps(file=file)
    joltage_step_count = dict(Counter(joltage_steps))
    submission = joltage_step_count[1] * joltage_step_count[3]

    return submission


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    joltage_list = list_joltages(file=file)

    arrangements = [1]
    step = 0
    for step, joltage in enumerate(joltage_list):
        arrangements.append(0)
        for back_step in range(step - 3, step):
            if back_step < 0:
                continue
            if joltage - joltage_list[back_step] < 4:
                arrangements[step] += arrangements[back_step]
    submission = arrangements[step]

    return submission


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    for file in INPUT_FILES:
        submission = process(file=Path(file))
        print(f'In file {file}, submission: {submission}')

    print('Part 2')

    for file in INPUT_FILES:
        submission = process_part2(file=Path(file))
        print(f'In file {file}, submission: {submission}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
