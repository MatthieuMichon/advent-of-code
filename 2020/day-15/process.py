#!/usr/bin/env python
"""
Advent of Code 2020: Day 15
"""

import os
import re
import signal
import sys
from types import FrameType
from typing import List, Mapping
from pathlib import Path


DEBUG = False


def spoken_number(starting_numbers: List[int], turns: int) -> int:
    """
    Compute spoken number after a given number of turns

    :param starting_numbers: list of starting numbers
    :param turns: number of rounds
    :return: spoken number
    """

    spoken_numbers = list()
    last_index = lambda li, n: next(i for i in reversed(range(len(li)))
                                    if li[i] == n)
    for turn, n in enumerate(starting_numbers):
        if DEBUG:
            print(f'Turn {1 + turn}: The number spoken is a starting number, {n}.')
        spoken_numbers.append(n)

    while 1 + turn < turns:
        turn += 1
        last_number = spoken_numbers[-1]
        spoken_before = last_number in spoken_numbers[:-1]
        new_spoken_number = 0 if not spoken_before else \
            turn - (1 + last_index(spoken_numbers[:-1], last_number))
        spoken_numbers.append(new_spoken_number)
        if DEBUG:
            print(f'Turn {1 + turn}: Last number spoken {last_number}, '
                  f'was {"" if spoken_before else "not"} spoken before. Number spoken {new_spoken_number}')

    return new_spoken_number


def spoken_number_part2(starting_numbers: List[int], turns: int) -> int:
    """
    Compute spoken number after a given number of turns (optimized)

    :param starting_numbers: list of starting numbers
    :param turns: number of rounds
    :return: spoken number
    """

    spoken_numbers = dict()
    last_number: int = 0
    last_number_spoken_before: bool = False
    turn: int = 0

    for i, n in enumerate(starting_numbers):
        if turn > 0:
            spoken_numbers[last_number] = turn
        turn = 1 + i
        if DEBUG:
            print(f'Turn {turn}: The number spoken is a starting number, {n}.')
        last_number = n
        last_number_spoken_before = last_number in spoken_numbers

    while turn < turns:
        turn += 1
        new_spoken_number = 0 if not last_number_spoken_before else \
            (turn - 1) - spoken_numbers[last_number]
        if DEBUG:
            print(f'Turn {turn}: Last number spoken {last_number}, '
                  f'was {"" if last_number_spoken_before else "not"} '
                  f'spoken before. Number spoken {new_spoken_number}')
        spoken_numbers[last_number] = turn - 1
        last_number = new_spoken_number
        last_number_spoken_before = last_number in spoken_numbers


    return last_number


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :param part_two: true for processing part 2
    :return: value to submit
    """

    debug = False

    numbers_list = [list(int(n) for n in l.strip().split(','))
                    for l in open(file)]
    number = 0
    for numbers in numbers_list:
        number = spoken_number(starting_numbers=numbers, turns=20200)

    submission = number
    return submission


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :param part_two: true for processing part 2
    :return: value to submit
    """

    debug = False

    numbers_list = [list(int(n) for n in l.strip().split(','))
                    for l in open(file)]
    number = 0
    for numbers in numbers_list:
        number = spoken_number_part2(starting_numbers=numbers, turns=30000000)

    submission = number
    return submission


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    file = './input.txt'
    submission = process(file=Path(file))
    print(f'In file {file}, submission: {submission}')

    print(f'Part 2')

    file = './input.txt'
    submission = process_part2(file=Path(file))
    print(f'In file {file}, submission: {submission}')

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


def install_signal_handler() -> None:
    """
    Install interrupt signal handler

    :return: nothing
    """

    signal.signal(signal.SIGINT, handle_sigint)


if __name__ == '__main__':
    install_signal_handler()
    sys.exit(main())
