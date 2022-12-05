#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2021 Edition - Day 8
Puzzle Solution in Python
"""

import logging
import sys
import time
from collections import Counter
from enum import Flag, auto
from functools import reduce
from itertools import chain, groupby
from operator import itemgetter
from pathlib import Path
from typing import Generator

from common.support import configure_logger, parse_arguments

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# Common Methods ---------------------------------------------------------------


def load_contents(filename: Path) -> Generator:
    """Load and convert contents from file

    :param filename: input filename
    :return: list of integers
    """
    with open(filename, encoding='utf-8') as buffer:
        for line in buffer.readlines():
            patterns, outputs = [part.strip().split(' ')
                                 for part in line.split('|')]
            yield patterns, outputs


# Solver Methods ---------------------------------------------------------------


def solve_part_one(contents: any) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    easy_digits = {
        1: 2,
        4: 4,
        7: 3,
        8: 7,
    }

    entries = list(zip(*contents))[1]
    easy_digit_count = 0
    for outputs in entries:
        easy_digit_count += sum(len(output) in easy_digits.values()
                                for output in outputs)
    answer = easy_digit_count
    return answer


class Segment(Flag):
    """Display segment enumeration class"""
    TOP = auto()
    UPPER_LEFT = auto()
    UPPER_RIGHT = auto()
    MIDDLE = auto()
    LOWER_LEFT = auto()
    LOWER_RIGHT = auto()
    BOTTOM = auto()


SEGMENTS_BY_DIGIT = {
    0: Segment.TOP | Segment.UPPER_LEFT | Segment.BOTTOM |
        Segment.LOWER_RIGHT | Segment.UPPER_RIGHT | Segment.LOWER_LEFT,
    1: Segment.UPPER_RIGHT | Segment.LOWER_RIGHT,
    2: Segment.TOP | Segment.MIDDLE | Segment.BOTTOM | Segment.UPPER_RIGHT |
       Segment.LOWER_LEFT,
    3: Segment.TOP | Segment.MIDDLE | Segment.BOTTOM |
        Segment.LOWER_RIGHT | Segment.UPPER_RIGHT,
    4: Segment.UPPER_LEFT | Segment.MIDDLE | Segment.UPPER_RIGHT |
        Segment.LOWER_RIGHT,
    5: Segment.TOP | Segment.UPPER_LEFT | Segment.MIDDLE | Segment.BOTTOM |
        Segment.LOWER_RIGHT,
    6: Segment.TOP | Segment.UPPER_LEFT | Segment.MIDDLE | Segment.BOTTOM |
        Segment.LOWER_RIGHT | Segment.LOWER_LEFT,
    7: Segment.TOP | Segment.UPPER_RIGHT | Segment.LOWER_RIGHT,
    8: Segment.TOP | Segment.UPPER_LEFT | Segment.MIDDLE | Segment.BOTTOM |
        Segment.LOWER_RIGHT | Segment.UPPER_RIGHT | Segment.LOWER_LEFT,
    9: Segment.TOP | Segment.UPPER_LEFT | Segment.MIDDLE | Segment.BOTTOM |
        Segment.LOWER_RIGHT | Segment.UPPER_RIGHT,
}

DIGIT_BY_SEGMENT = {v: k for k, v in SEGMENTS_BY_DIGIT.items()}
NB_SEGMENTS_BY_DIGIT = {k: len(v) for k, v in SEGMENTS_BY_DIGIT.items()}
DIGITS_BY_NB_SEGMENTS = {k: [ch for ch, _ in v] for k, v in
                        groupby(sorted(NB_SEGMENTS_BY_DIGIT.items(),
                                       key=itemgetter(1)), itemgetter(1))}
DIGITS_BY_SEGMENT = {k: [d for d, v in SEGMENTS_BY_DIGIT.items() if k in v]
                     for k in Segment}
OCCURRENCES_BY_SEGMENT = {k: len(v) for k, v in DIGITS_BY_SEGMENT.items()}
SEGMENTS_BY_OCCURRENCE = {k: [ch for ch, _ in v] for k, v in
                          groupby(sorted(OCCURRENCES_BY_SEGMENT.items(),
                                         key=itemgetter(1)), itemgetter(1))}

EXPECTED_NB_SEGMENTS = 10


def map_digits(digits: list) -> dict:
    """Map digits to segments

    :param digits: list of digits combinations
    :return: per-character segment map
    """

    # map segment by char for segments with unique occurrence

    char_occurrences = Counter(chain.from_iterable(digits))
    segment_by_char = {}
    for char, occurrence in char_occurrences.items():
        ambiguous_char = (1 != len(SEGMENTS_BY_OCCURRENCE[occurrence]))
        if ambiguous_char:
            continue
        segment_by_char[char] = SEGMENTS_BY_OCCURRENCE[occurrence][0]

    # find digits with unique segment number

    for enabled_chars in sorted(digits, key=len):
        nb_segments = len(enabled_chars)
        ambiguous_digit = (1 != len(DIGITS_BY_NB_SEGMENTS[nb_segments]))
        if ambiguous_digit:
            continue
        digit = DIGITS_BY_NB_SEGMENTS[nb_segments][0]
        unresolved_chars = set(enabled_chars) - set(segment_by_char.keys())
        for char in enabled_chars:
            already_resolved = (char not in unresolved_chars)
            if already_resolved:
                continue
            if 1 == len(unresolved_chars):
                segment = SEGMENTS_BY_DIGIT[digit] & ~ reduce(Flag.__or__, segment_by_char.values())
                segment_by_char[char] = segment
    return segment_by_char


def map_number(numbers: list, char_map: dict) -> int:
    """Map list of numbers into an integer

    :param numbers:
    :param char_map:
    :return:
    """
    mapped_number_str = ''
    for digit in numbers:
        segments = reduce(Flag.__or__, [char_map[s] for s in digit])
        mapped_number_str += str(DIGIT_BY_SEGMENT[segments])
    return int(mapped_number_str)


def solve_part_two(contents: any) -> int:
    """Solve the second part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    answer = 0
    for digits, output_value in contents:
        char_map = map_digits(digits=digits)
        number = map_number(numbers=output_value, char_map=char_map)
        answer += number
    return answer


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """
    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'called with {args=}')
    start_time = time.perf_counter()
    contents = list(load_contents(filename=args.filename))
    compute_part_one = not args.part or args.part == 1
    answer_part_one = 0
    if compute_part_one:
        answer_part_one = solve_part_one(contents=contents)
    compute_part_two = not args.part or 2 == args.part
    answer_part_two = 0
    if compute_part_two:
        answer_part_two = solve_part_two(contents=contents)
    elapsed_time = time.perf_counter() - start_time
    print(f'{answer_part_one=}')
    print(f'{answer_part_two=}')
    print(f'done in {1000 * elapsed_time:0.1f} milliseconds')
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
