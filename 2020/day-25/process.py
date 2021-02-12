#!/usr/bin/env python

"""Advent of Code 2020

Day 25: Combo Breaker
"""

import os
import sys
from pathlib import Path


def load_public_keys(file: Path) -> tuple[int]:
    """Load public keys from a given file

    :param file: file containing the keys
    :return: public keys as a tuple of int
    """
    public_keys_str = open(file).read().strip().split(os.linesep)
    public_keys = tuple(int(k) for k in public_keys_str)
    return public_keys


def transform(subject_number: int, loop_size: int) -> int:
    """Transform a subject number and loop size into a public key

    :param subject_number: transformation input value
    :param loop_size: number of iterations
    :return: key value
    """
    value = subject_number**loop_size % 20201227
    return value


def compute_encryption_key(public_keys: tuple) -> int:
    """Compute the common encryption key

    :param public_keys: public keys
    :return: encryption key as integer
    """
    card_pk, door_pk = public_keys
    loop_size: int = 0
    loop_size_factor = 7
    while loop_size_factor % 20201227 != card_pk:
        loop_size += 1
        loop_size_factor *= 7
    loop_size += 1
    encryption_key = transform(subject_number=door_pk, loop_size=loop_size)
    return encryption_key


def print_part_one(inputs: list[Path]) -> None:
    """Print answer for part one

    :param inputs: list of puzzle input files
    :return: nothing
    """
    for file in inputs:
        pk = load_public_keys(file=file)
        key = compute_encryption_key(public_keys=pk)
        print(f'Day 25 part one, file: {file}; answer: {key}')
        assert key == 14897079


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
