#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 11
Puzzle Solution in Python
"""

import argparse
import logging
import os
import sys

from enum import Enum, IntEnum, auto
from typing import Iterator

log = logging.getLogger(__name__)


class Colors(IntEnum):
    BLACK = 0
    WHITE = 1


class Turns(IntEnum):
    LEFT = 0
    RIGHT = 1


class Directions(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class HaltOpcode(Error):
    """Exception when an HALT opcode is encountered.

    Attributes:
        opcode -- opcode value
    """

    def __init__(self):
        super().__init__()


class OpcodeError(Error):
    """Exception raised for unsupported opcode.

    Attributes:
        opcode -- opcode value
    """

    def __init__(self, opcode: int):
        message = f'Invalid opcode {opcode}'
        super().__init__(message)


# Common Methods ---------------------------------------------------------------


def load_contents(filename: str) -> Iterator[map]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding a list of integers
    """
    lines = open(filename).read().strip().split(os.linesep)
    for line in lines:
        yield {i: int(token) for i, token in enumerate(line.split(','))}


# Solver Methods ---------------------------------------------------------------


def paint_panel(panels: map, color: int, robot: map, turn: int) -> None:
    """Paint panel and move the robot

    :param panels: map of panels
    :param color: direction to turn to after advancing
    :param robot: robot state
    :param turn: direction to turn to after advancing
    :return: nothing
    """
    robot['trail'].append(robot['x'], robot['y'])
    heading = robot['heading']
    if heading == Directions.NORTH:
        robot['y'] += 1
    if heading == Directions.EAST:
        robot['x'] += 1
    if heading == Directions.SOUTH:
        robot['y'] -= 1
    if heading == Directions.WEST:
        robot['x'] += 1
    if turn == Turns.LEFT:
        robot['heading'] = (robot['heading'] - 1) % 4
    if turn == Turns.RIGHT:
        robot['heading'] = (robot['heading'] + 1) % 4


def step(ram: dict, pc: int, inputs: list[int]) -> tuple[int, tuple]:
    ...
    return pc, (Colors.WHITE, Turns.LEFT)


def solve(contents: map) -> int:
    """Solve puzzle part one

    :param contents: puzzle input contents
    :return: puzzle answer
    """
    robot = {
        'position': (0, 0),
        'heading': Directions.NORTH,
        'trail': []
    }
    pc = 0
    panels = dict()
    try:
        while True:
            color = panels.get(robot['position'], Colors.BLACK)
            pc, outputs = step(ram=contents, pc=pc, inputs=[color])
            new_color, turn = outputs
            paint_panel(panels=panels, color=new_color, robot=robot, turn=turn)
    except HaltOpcode:
        ...

    answer = len(set(robot['trail']))
    return answer


def solve_part_two(contents: map) -> int:
    """Solve puzzle part two

    :param contents: puzzle input contents
    :return: puzzle answer
    """
    answer = -1
    return answer


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
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
        contents = next(load_contents(filename=args.filename))
        answer = solve(contents=contents)
        print(f'part one: {answer=}')
    if compute_part_two:
        answer = -1  # TODO
        print(f'part two: {answer=}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
