#!/usr/bin/env python
"""
Advent of Code 2020 - Day 6: Custom Customs
"""
import sys
from pathlib import Path
import bisect

from typing import Iterator, List


INPUT_FILES = ['./short-input.txt', './input.txt']


def split_groups(file: Path) -> Iterator[str]:
    """
    Split input file into groups

    :param file: custom declaration file to process
    :return: generator yielding a list of fields
    """

    group_answers = ''
    for line in open(file):
        if line == '\n':
            yield group_answers
            group_answers = ''
            continue
        group_answers += line.strip()
    yield group_answers


def process_custom_declarations(file: Path, verbose: bool) -> int:
    """
    Process a given custom declaration file

    :param file: custom declaration file to process
    :param verbose: print extra information
    :return: sum of yes answers
    """

    sum_yes_answers = 0
    for group_answers in split_groups(file=file):
        unique_answers = ''.join(set(group_answers))
        if verbose:
            print(f'group answers: {group_answers}, unique answers {unique_answers}')
        sum_yes_answers += len(unique_answers)
    return sum_yes_answers


def split_groups_part2(file: Path) -> Iterator[List]:
    """
    Split input file into groups

    :param file: custom declaration file to process
    :return: generator yielding a list of fields
    """

    group_answers = list()
    for line in open(file):
        if line == '\n':
            yield group_answers
            group_answers = list()
            continue
        group_answers.append(line.strip())
    yield group_answers


def process_custom_declarations_part2(file: Path, verbose: bool) -> int:
    """
    Process a given custom declaration file

    :param file: custom declaration file to process
    :param verbose: print extra information
    :return: sum of yes answers
    """

    sum_all_yes_answers = 0
    for group_answers in split_groups_part2(file=file):
        if len(group_answers) == 1:
            all_yes_answers = len(group_answers[0])
        else:
            all_yes_answers = sum(1 for c in group_answers[0] if all(c in answer for answer in group_answers[1:]))
        if verbose:
            print(f'group answers: {group_answers}, unique answers {all_yes_answers}')
        sum_all_yes_answers += all_yes_answers
    return sum_all_yes_answers


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    for file in INPUT_FILES:
        verbose = 'short' in file
        sum_yes_answers = process_custom_declarations(
            file=Path(file), verbose=verbose)
        print(f'In file {file}, sum of yes answers: {sum_yes_answers}')

    print('Part 2')

    for file in INPUT_FILES:
        verbose = 'short' in file
        sum_all_yes_answers = process_custom_declarations_part2(
            file=Path(file), verbose=verbose)
        print(f'sum all yes answers: {sum_all_yes_answers}')

    return 0


if __name__ == '__main__':
    """
    Command line entry-point
    """
    sys.exit(main())
