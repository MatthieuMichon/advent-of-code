#!/usr/bin/env python

"""Advent of Code 2020

Day 25: Combo Breaker
"""

import itertools
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator

# Common -----------------------------------------------------------------------


def load_public_keys(file: Path) -> tuple[int]:
    """Load public keys from a given file

    :param file: file containing the keys
    :return: public keys as a tuple of int
    """
    public_keys_str = open(file).read().strip().split(os.linesep)
    public_keys = tuple(int(k) for k in public_keys_str)
    return public_keys


# Part One  --------------------------------------------------------------------


def print_part_one(inputs: list[Path]) -> None:
    """Print answer for part one

    :param inputs: list of puzzle input files
    :return: nothing
    """
    for file in inputs:
        pk = load_public_keys(file=file)
        print(f'Day 24 part one, file: {file}; answer: {pk}')


# Common -----------------------------------------------------------------------


def main() -> int:
    """Main function

    :return: shell exit code
    """
    inputs = [
        'example.txt',
        'input.txt'
    ]
    print_part_one(inputs=[Path(i) for i in inputs])
    return 0


if __name__ == '__main__':
    sys.exit(main())
