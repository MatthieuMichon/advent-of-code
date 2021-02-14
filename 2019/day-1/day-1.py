#!/usr/bin/env python

import argparse
import logging
import os
import sys
from pathlib import Path


EXIT_SUCCESS = 0
LOG_FORMAT = ('%(asctime)s - %(levelname)s - %(module)s - '
              '%(funcName)s - %(message)s')

log = logging.getLogger(__name__)


def load_contents(filename: Path) -> list[int]:
    """Load contents from the given file

    :param filename: filename as string
    :return: list of integers
    """
    contents = list(map(int, open(filename).read().strip().split(os.linesep)))
    log.info(f'Loaded {len(contents)} values from file {filename}')
    return contents


def solve(contents: list[int]):
    """Solve part one of the puzzle

    :param contents: list of integers
    :return: answer for the part one of the puzzle
    """

    def compute_required_fuel(mass: int) -> int:
        """Compute required fuel from a mass

        :param mass: mass value
        :return: fuel value
        """
        required_fuel = mass // 3 - 2
        return required_fuel

    mass_values = contents
    fuel_values = [compute_required_fuel(mass) for mass in mass_values]
    answer = sum(fuel_values)
    return answer


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
    parser = argparse.ArgumentParser()
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
    contents = load_contents(filename=Path(args.filename))
    answer = solve(contents=contents)
    print(answer)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
