#!/usr/bin/env python
"""
Advent of Code 2020 - Day 2: Password Philosophy
"""
import argparse
import os
import sys
from collections import Counter
from pathlib import Path
from typing import List


def filter_valid_passwords(file: Path) -> List[str]:
    """
    Return only valid passwords from the ones listed in a file

    :param file: password list file
    :return: password meeting requirements
    """

    for line in open(file):
        min_max, char, password = line.strip().split(' ')
        min, max = [int(part) for part in min_max.split('-')]
        char = char[0]
        cnt = Counter(c for c in password)
        if min <= cnt[char] <= max:
            yield password


def filter_valid_passwords_part2(file: Path) -> List[str]:
    """
    Filter function for part 2 of the challenge

    :param file: password list file
    :return: password meeting requirements
    """

    for line in open(file):
        min_max, char, password = line.strip().split(' ')
        first_index, second_index = [int(part) - 1
                                     for part in min_max.split('-')]
        char = char[0]
        if (password[first_index] == char) ^ (password[second_index] == char):
            yield password


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('password_file', type=str,
                        help='Password file to inspect')
    args = parser.parse_args()

    password_file = Path(args.password_file)
    if not os.path.isfile(password_file):
        raise FileNotFoundError(f'File {password_file} does not exists')

    valid_passwords = filter_valid_passwords(file=password_file)

    print(f'Found {len(list(valid_passwords))} passwords')

    valid_passwords = filter_valid_passwords_part2(file=password_file)

    print(f'Found {len(list(valid_passwords))} passwords for part 2')

    return 0


if __name__ == '__main__':
    """
    Command line entry-point
    """
    sys.exit(main())
