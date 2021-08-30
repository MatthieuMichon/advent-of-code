#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 10
Puzzle Solution in Python
"""

import argparse
import logging
import os
import sys

from pathlib import Path
from typing import Iterator

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def load_contents(file: Path) -> Iterator:
    """Load and convert contents from a filename

    :param file: input file handle
    :return: iterator yielding a dict entry for each chemical reaction
    """
    _EQ_OPERATOR = ' => '
    _LHS_SEPARATOR = ', '
    _CHEM_SEPARATOR = ' '

    def split_lhs(lhs: str) -> Iterator:
        chems = lhs.split(_LHS_SEPARATOR)
        for chem in chems:
            yield split_chem(chem)

    def split_chem(chem: str) -> (int, str):
        qty, name = chem.split(_CHEM_SEPARATOR)
        qty = int(qty)
        return qty, name

    lines = open(file).read().strip().split(os.linesep)
    assert all(_EQ_OPERATOR in l for l in lines)
    log.info(f'Loaded {len(lines)} lines from {file=}')
    for l in lines:
        lhs, rhs = l.split(_EQ_OPERATOR)
        lhs = tuple(split_lhs(lhs))
        rhs_qty, rhs_name = tuple(split_chem(rhs))
        yield rhs_name, {'qty': rhs_qty, 'lhs': lhs}


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
EXIT_ERROR = 1
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


def configure_logger(verbose: bool):
    """Configure logging

    :param verbose: display debug and info messages
    :return: nothing
    """
    logger = logging.getLogger()
    logger.handlers = []
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(level=logging.WARNING)
    stdout.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(stdout)
    if verbose:
        stdout.setLevel(level=logging.DEBUG)
        logger.setLevel(level=logging.DEBUG)


def parse_arguments() -> argparse.Namespace:
    """Parse arguments provided by the command-line

    :return: list of decoded arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    pa = parser.add_argument
    pa('filename', type=str, help='input contents filename')
    pa('-p', '--part', type=int, help='solve only the given part')
    pa('-v', '--verbose', action='store_true', help='print extra messages')
    arguments = parser.parse_args()
    return arguments


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """
    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'Arguments: {args}')
    compute_part_one = not args.part or 1 == args.part
    compute_part_two = not args.part or 2 == args.part
    if compute_part_one:
        contents = {k: v for k, v in
                    load_contents(file=Path(args.filename))}
        print(contents)
        return EXIT_ERROR
        print(f'part one: answer: {answer}')
    if compute_part_two:
        return EXIT_ERROR
        print(f'part two: answer: {answer}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
