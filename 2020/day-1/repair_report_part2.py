#!/usr/bin/env python
"""
Advent of Code 2020 - Day 1: Report Repair - Part 2
"""

import argparse
import functools
import itertools
import os
import sys

from pathlib import Path
from typing import List


NULL_SEARCH = (None, None, None)


def search_expenses(expense_list: List[int]) -> tuple:
    """
    Search expense list for pair matching the sum requirement

    :param expense_list: list of expenses
    :return: triplet of nulls or integers matching required total
    """

    for triplet in itertools.permutations(expense_list, 3):
        if sum(triplet) == 2020:
            return triplet

    return NULL_SEARCH


def repair(file: Path) -> any:
    """
    Repair the given file by finding the incorrect expense entry triplet

    :param file: report file to repair
    :return: product of the incorrect expenses
    """

    with open(file) as fp:
        expenses = []
        for line in fp.readlines():
            if not len(line.strip()):
                continue
            expenses.append(int(line))

    triplet = search_expenses(expenses)
    if NULL_SEARCH == triplet:
        return None
    product = functools.reduce(lambda x, y: x * y, triplet)

    return product


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report_file', type=str, help='Report file to repair')
    args = parser.parse_args()

    report_file = Path(args.report_file)
    if not os.path.isfile(report_file):
        raise FileNotFoundError(f'File {report_file} does not exists')

    product = repair(file=report_file)
    if not product:
        print(f'Failed to locate pair')
        return 1

    print(f'Found product: {product}')
    return 0


if __name__ == '__main__':
    """
    Command line entry-point
    """
    sys.exit(main())
