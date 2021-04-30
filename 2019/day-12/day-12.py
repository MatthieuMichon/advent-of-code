#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 12
Puzzle Solution in Python
"""

import argparse
import logging
import math
import os
import sys

from itertools import permutations
from typing import Iterator

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def load_contents(filename: str) -> Iterator[map]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding a list of integers
    """
    lines = open(filename).read().strip().strip('<>').split(os.linesep)
    for line in lines:
        axis = [token.split('=') for token in line.strip('<>').split(',')]
        axis = {name: int(value) for name, value in axis}
        yield axis


def trace(step: int, positions: list[map], velocities: list[map]) -> None:
    """Trace values

    :param step: step index
    :param positions: bodies positions
    :param velocities: bodies velocity
    :return: nothing
    """
    log.info(f'{step=}')
    for i, pos in enumerate(positions):
        vel = velocities[i]
        log.info(f'{pos=}, {vel=}')


PERMUTATIONS = list(permutations(range(4), 2))


def compute_time_step(positions: list[map], velocities: list[map]) -> None:
    """Update positions and velocities

    :param positions: bodies positions
    :param velocities: bodies velocity
    :return: nothing
    """
    # bodies = range(len(positions))
    # for ref, opp in permutations(bodies, 2):

    # FIXME: iterate over each axis first
    for ref, opp in PERMUTATIONS:
        ref_pos = positions[ref].items()
        opp_pos = positions[opp]
        for axis, ref_val in ref_pos:
            opp_val = opp_pos[axis]
            if ref_val < opp_val:
                velocities[ref][axis] += 1
            elif ref_val > opp_val:
                velocities[ref][axis] -= 1
    for body, pos in enumerate(positions):
        for axis in pos.keys():
            pos[axis] += velocities[body][axis]


def step_by_axis(
        positions: list[int], velocities: list[int]) -> None:
    """Update positions and velocities

    :param positions: bodies positions
    :param velocities: bodies velocity
    :return: nothing
    """
    for index, body in enumerate(positions):
        velocities[index] += \
            sum(opp > body for opp in positions) - \
            sum(body > opp for opp in positions)
    for index, body in enumerate(positions):
        positions[index] += velocities[index]


def compute_total_energy(positions: list[map], velocities: list[map]) -> int:
    """Compute total energy

    :param positions: bodies positions
    :param velocities: bodies velocity
    :return: total energy
    """
    total_energy = 0
    for body, pos in enumerate(positions):
        body_energy = sum(map(abs, pos.values()))
        kin = velocities[body]
        body_energy *= sum(map(abs, kin.values()))
        total_energy += body_energy
    return total_energy


# Solver Methods ---------------------------------------------------------------


def solve(contents: list[map], steps: int) -> int:
    """Part one solving method

    :param contents: decoded contents
    :param steps: number of steps to compute
    :return: answer
    """
    positions = contents
    velocities = [{axis: 0 for axis in body.keys()} for body in positions]
    for step in range(steps):
        if not step % 10:
            trace(step, positions, velocities)
        compute_time_step(positions, velocities)
    total_energy = compute_total_energy(positions, velocities)
    return total_energy


def solve_part_two(contents: list[map]) -> int:
    """Part two solving method

    :param contents: decoded contents
    :return: answer
    """
    def lcm(a: int, b: int) -> int:
        return int((a * b) / math.gcd(a, b))

    pos_per_axis = [[body[axis] for body in contents] for axis in contents[0].keys()]
    vel_per_axis = [0 for _ in range(4)]
    cycles_per_axis = list()
    for axis, positions in enumerate(pos_per_axis):
        step = 0
        while True:
            step += 1
            step_by_axis(positions=positions, velocities=vel_per_axis)
            if all(axis == 0 for axis in vel_per_axis):
                print(f'{step=}')
                cycles_per_axis.append(step)
                break
    answer = 2 * lcm(lcm(cycles_per_axis[0], cycles_per_axis[1]), cycles_per_axis[2])
    return answer


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


def configure_logger(level: int):
    """Configure logging

    :param level: verbosity level
    :return: nothing
    """
    logger = logging.getLogger()
    logger.handlers = []
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(level=logging.WARNING)
    stdout.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(stdout)
    if level >= 2:
        stdout.setLevel(level=logging.DEBUG)
        logger.setLevel(level=logging.DEBUG)
    elif level >= 1:
        stdout.setLevel(level=logging.INFO)
        logger.setLevel(level=logging.INFO)


def parse_arguments() -> argparse.Namespace:
    """Parse arguments provided by the command-line

    :return: list of decoded arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    pa = parser.add_argument
    pa('filename', type=str, help='input contents filename')
    pa('-p', '--part', type=int, help='solve only the given part')
    pa('-v', '--verbose', action='count', default=0)
    arguments = parser.parse_args()
    return arguments


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """
    args = parse_arguments()
    configure_logger(level=args.verbose)
    log.info(f'Arguments: {args}')
    compute_part_one = not args.part or 1 == args.part
    compute_part_two = not args.part or 2 == args.part
    contents = list(load_contents(filename=args.filename))
    if compute_part_one:
        answer = solve(contents=contents, steps=1000)
        print(f'part one: {answer=}')
    if compute_part_two:
        answer = solve_part_two(contents=contents)
        print(f'part two: {answer=}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
