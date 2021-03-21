#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 8
Puzzle Solution in Python
"""

import argparse
import json
import logging
import sys
from collections import Counter
log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def load_contents(filename: str) -> map:
    """Load and convert contents from file

    :param filename: input filename
    :return: contents map
    """
    contents = json.load(fp=open(filename))
    return contents


def splice_data(data: str, width: int, height: int) -> list[str]:
    """Splice a data chunk into a number of layers

    :param data: Image pixels
    :param width: Image width in pixels
    :param height: Image height in pixels
    :return: List of layer of pixels
    """
    layer_length = width * height
    assert 0 == len(data) % layer_length
    layers = list()
    for i in range(0, len(data), layer_length):
        layers.append(data[i:i + layer_length])
    return layers


def flatten(pixel: str) -> str:
    """Flatten layers into a single value

    :param pixel: list of layers as string
    :return: color
    """
    for layer in pixel:
        if layer != '2':
            return layer


# Puzzle Solving Methods -------------------------------------------------------


def solve(contents: map) -> int:
    """Solve part one of the puzzle

    :param contents: decoded puzzle contents
    :return: answer for the part one of the puzzle
    """
    layers = splice_data(**contents)
    occurrences = [Counter(l)['0'] for l in layers]
    layer_least_zeroes = occurrences.index(min(occurrences))
    layer_least_zeroes_occurrence = Counter(layers[layer_least_zeroes])
    answer = layer_least_zeroes_occurrence['1'] \
        * layer_least_zeroes_occurrence['2']
    return answer


def solve_part_two(contents: map) -> int:
    """Solve part two of the puzzle

    :param contents: decoded puzzle contents
    :return: answer for the part two of the puzzle
    """
    layers = splice_data(**contents)
    layers_per_pixel = [''.join(l) for l in list(zip(*layers))]
    pixels = list(map(flatten, layers_per_pixel))
    pixels = [' ' if p == '0' else '#' for p in pixels]
    for i in range(0, len(pixels), contents['width']):
        print(f'{"".join(pixels[i:i+contents["width"]])}')
    answer = -1
    return answer


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-32s - %(levelname)-8s - %(message)s'


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
        contents = load_contents(filename=args.filename)
        answer = solve(contents=contents)
        print(f'part one: answer: {answer}')
    if compute_part_two:
        contents = load_contents(filename=args.filename)
        answer = solve_part_two(contents=contents)
        #print(f'part two: answer: {answer}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
