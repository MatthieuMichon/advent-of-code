#!/usr/bin/env python
"""
Advent of Code 2020 - Day 4: Passport Processing
"""
import sys
from pathlib import Path
from typing import Iterator, Mapping


PASSPORT_FILES = ['./short-input.txt', './input.txt']
REQUIRED_FIELDS = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    # 'cid',
]


def split_passports(file: Path) -> Iterator[Mapping]:
    """
    Split a given passport file

    :param file: passport file to process
    :return: generator yielding a list of fields
    """

    passport = {}
    for line in open(file):
        if line == '\n':
            yield passport
            passport = {}
            continue
        fields = line.strip().split(' ')
        passport.update({k:v for k, v in [f.split(':') for f in fields]})
    yield passport


def process_passports(file: Path) -> int:
    """
    Process a given passport file

    :param file: passport file to process
    :return: number of valid passports
    """

    valid_passports = 0
    for passport in split_passports(file=file):
        if all(f in passport.keys() for f in REQUIRED_FIELDS):
            valid_passports += 1

    return valid_passports


def validate_strict(passport: Mapping) -> bool:
    """
    Do strict validation of the given passport

    :param passport: passport map to validate
    :return: True if validation succeeded
    """

    if not 1920 <= int(passport['byr']) <= 2002:
        return False
    if not 2010 <= int(passport['iyr']) <= 2020:
        return False
    if not 2020 <= int(passport['eyr']) <= 2030:
        return False
    hgt = passport['hgt']
    if ('cm' in hgt) and (not 150 <= int(hgt[:-2]) <= 193):
        return False
    elif ('in' in hgt) and (not 59 <= int(hgt[:-2]) <= 76):
        return False
    elif not any(un in hgt for un in ['cm', 'in']):
        return False
    hcl = passport['hcl']
    if hcl[0] != '#':
        return False
    try:
        int(hcl[1:], 16)
    except ValueError:
        return False
    if 1 != sum(
            1 for color in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
           if color == passport['ecl']):
        return False
    if 9 != len(passport['pid']):
        return False

    return True


def process_passports_part2(file: Path) -> int:
    """
    Process a given passport file

    :param file: passport file to process
    :return: number of valid passports
    """

    valid_passports = 0
    for passport in split_passports(file=file):
        if all(f in passport.keys() for f in REQUIRED_FIELDS):
            if validate_strict(passport=passport):
                valid_passports += 1

    return valid_passports


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    for file in PASSPORT_FILES:
        valid_passports = process_passports(file=Path(file))
        print(valid_passports)

    print('Part 2')

    for file in PASSPORT_FILES:
        valid_passports = process_passports_part2(file=Path(file))
        print(valid_passports)

    return 0


if __name__ == '__main__':
    """
    Command line entry-point
    """
    sys.exit(main())
