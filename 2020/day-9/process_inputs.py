#!/usr/bin/env python
"""
Advent of Code 2020 - Day 9: Encoding Error
"""
import re
import sys
import itertools
from pathlib import Path
from typing import List, Generator

INPUT_FILES = ['./short-input.txt', './input.txt']


def decode(file: Path) -> List:
    """
    Decode the given file

    :param file: file to process
    :return: string and int tuple
    """

    ret = list()
    for line in open(file):
        m = re.search(r'^(?P<op>\w{3}) (?P<arg>[+-]\d+)$', line)
        if not m:
            raise Exception(f'{line}')
        d = m.groupdict()
        ret.append([d['op'], int(d['arg'])])
    return ret


def list_n_previous_numbers(file: Path, window: int) -> Generator:
    previous_numbers = []
    for line in open(file):
        if len(previous_numbers) >= window:
            yield previous_numbers[-window:], int(line)
        previous_numbers.append(int(line))


def execute(instruction: List) -> tuple:
    op, arg = instruction
    if op == 'nop':
        return 1, 0
    if op == 'jmp':
        return arg, 0
    if op == 'acc':
        return 1, arg


def process(file: Path) -> tuple[int, int]:
    """
    Process the given file

    The first step of attacking the weakness in the XMAS data is to find the
    first number in the list (after the preamble) which is not the sum of two
    of the 25 numbers before it. What is the first number that does not have
    this property?

    :param file: custom declaration file to process
    :return: answer
    """

    window = 25 if 'short' not in file.stem else 5

    for index, (n_previous, sum_) in enumerate(list_n_previous_numbers(file=file, window=window)):
        combs = itertools.combinations(n_previous, 2)
        if not any(sum(pair) == sum_ for pair in combs):
            print(f'At index {index}')
            return sum_
    raise Exception('Failed to find solution')


def process_part2(file: Path) -> int:
    """
    Process the given file

    The first step of attacking the weakness in the XMAS data is to find the
    first number in the list (after the preamble) which is not the sum of two
    of the 25 numbers before it. What is the first number that does not have
    this property?

    :param file: custom declaration file to process
    :return: answer
    """

    window = 25 if 'short' not in file.stem else 5

    for index, (n_previous, sum_) in enumerate(list_n_previous_numbers(file=file, window=window)):
        combs = itertools.combinations(n_previous, 2)
        if not any(sum(pair) == sum_ for pair in combs):
            print(f'At index {index}')
            break

    invalid_number = sum_
    for window in range(2, invalid_number):
        for n_previous, _ in list_n_previous_numbers(file=file, window=window):
            if sum(n_previous) == invalid_number:
                print(f'Found set {n_previous}')
                min_ = min(n_previous)
                max_ = max(n_previous)
                return min_ + max_


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


if __name__ == '__main__':
    """
    Command line entry-point
    """
    sys.exit(main())
