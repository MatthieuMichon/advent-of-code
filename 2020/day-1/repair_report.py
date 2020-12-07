#!/usr/bin/env python
"""
Advent of Code 2020 - Day 1: Report Repair
"""
import argparse
import bisect
import os
import sys

from pathlib import Path
from typing import List

NULL_SEARCH = (None, None)
HALF_VALUE = 2020 / 2


def search_expenses(expense_list: List[int]) -> tuple:
    """
    Search expense list for pair matching the sum requirement

    :param expense_list: list of expenses
    :return: null or pair of integers matching required total
    """

    mid_index = bisect.bisect(expense_list, HALF_VALUE)
    if not mid_index or mid_index == len(expense_list):
        return NULL_SEARCH

    lower_half = expense_list[:mid_index]
    upper_half = expense_list[mid_index:]

    for lower in lower_half:
        for higher in upper_half:
            if 2020 == lower + higher:
                return lower, higher

    return NULL_SEARCH


def repair(file: Path) -> any:
    """
    Repair the given file by finding the incorrect expense entry pair

    :param file: report file to repair
    :return: tuple representing the incorrect expenses
    """

    with open(file) as fp:
        even_amount_expenses = []
        odd_amount_expenses = []
        even = lambda a: True == (a % 2)
        def product(tuple_): return tuple_[0] * tuple_[1]

        for line in fp.readlines():
            if not len(line.strip()):
                continue
            amount = int(line)
            if even(amount):
                bisect.insort(even_amount_expenses, amount)
                pair = search_expenses(even_amount_expenses)
                if NULL_SEARCH != pair:
                    result = product(pair)
                    return result
            else:
                bisect.insort(odd_amount_expenses, amount)
                pair = search_expenses(odd_amount_expenses)
                if NULL_SEARCH != pair:
                    result = product(pair)
                    return result

    return None


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
