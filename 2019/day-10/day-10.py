#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 10
Puzzle Solution in Python
"""

import argparse
import cmath
import logging
import os
import sys

from typing import Iterator

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def load_contents(filename: str) -> Iterator[set]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding maps of boolean per coordinates
    """
    lines = open(filename).read().strip().split(os.linesep)
    positions = set()
    y = 0
    for line in lines:
        if not len(line):
            log.debug(f'{filename=}, map of {len(positions)} items')
            yield positions
            positions = set()
            y = 0
            continue
        positions.update({(x, y) for x, c in enumerate(line) if c == '#'})
        y += 1
    log.debug(f'{filename=}, map of {len(positions)} items')
    yield positions


def compute_offsets(reference: tuple[int, int],
                    asteroids: set[tuple[int, int]]) -> set[tuple]:
    """Computing offsets o asteroids with regard to a given reference

    :param reference: reference coordinates
    :param asteroids: list of asteroids
    :return: list of asteroids with offset coordinates
    """
    offsets = set()
    for asteroid in asteroids:
        t = tuple(a - b for a, b in zip(reference, asteroid))
        offsets.add(t)
    return offsets


def map_detected_asteroids(asteroids: set) -> map:
    """Compute number of detected asteroids from each asteroid position

    :param asteroids: list of asteroids
    :return: map of detected asteroids per location
    """
    detected_asteroids_map = dict()
    for asteroid in asteroids:
        others = asteroids - {asteroid}
        polar_positions = compute_positions(reference=asteroid,
                                            asteroids=others)
        angles = set(angle for distance, angle in polar_positions)
        detected_asteroids_map[asteroid] = len(angles)
    return detected_asteroids_map


def compute_positions(reference: tuple, asteroids: set[tuple]) -> set:
    """Compute polar positions relative to a reference

    :param reference: reference position in Cartesian coordinates
    :param asteroids: list of asteroids in absolute Cartesian coordinates
    :return: list of asteroids in relative polar coordinates
    """
    positions = set()
    assert reference not in asteroids
    rel_positions = compute_offsets(reference=reference, asteroids=asteroids)
    for pos in rel_positions:
        distance, angle = cmath.polar(complex(*pos))
        positions.add((distance, angle))
    return positions


def map_polar_pos(reference: tuple, asteroids: set[tuple]) -> dict[float, dict]:
    """Map a list of polar positions by angle and distance

    :param reference: reference position in Cartesian coordinates
    :param asteroids: list of asteroids in absolute Cartesian coordinates
    :return: per-angle map of per-distance asteroids
    """
    position_map = dict()
    for asteroid in asteroids:
        relative_x = asteroid[0] - reference[0]
        relative_y = asteroid[1] - reference[1]
        transformed_pos = (-relative_y, relative_x)
        distance, angle = cmath.polar(complex(*transformed_pos))
        if angle < 0:
            angle += 2 * cmath.pi
        angle *= 180.0 / cmath.pi
        if angle not in position_map:
            position_map[angle] = {distance: asteroid}
        else:
            position_map[angle].update({distance: asteroid})
    log.debug(f'mapped {len(position_map)} angles')
    position_map = dict(sorted(position_map.items(), key=lambda item: item[0]))
    for angle, distance in position_map.items():
        distance = dict(sorted(distance.items(), key=lambda item: item[0]))
        position_map[angle] = distance
    for deg in range(0, 360, 90):
        log.debug(f'at {deg=} {len(position_map[deg])}')
    return position_map


def vaporize(station: tuple, asteroids: set[tuple], quantity: int) -> tuple:
    """Vaporize a number of asteroids and return position of the last one

    :param station: vaporization station position in Cartesian coordinates
    :param asteroids: list of asteroids in absolute Cartesian coordinates
    :param quantity: number of asteroid to vaporize
    :return: position of the last vaporized asteroid
    """
    polar_map = map_polar_pos(reference=station, asteroids=asteroids)
    scan_angle = next(iter(polar_map.keys()))
    asteroid = (0, 0)
    for _ in range(quantity):
        log.debug(f'{scan_angle=}')
        asteroids_by_distance = polar_map[scan_angle]
        scan_index = list(polar_map.keys()).index(scan_angle)
        next_scan_index = (1 + scan_index) % len(polar_map)
        next_scan_angle = list(polar_map.keys())[next_scan_index]
        closest_distance = next(iter(asteroids_by_distance.keys()))
        asteroid = asteroids_by_distance.pop(closest_distance)
        log.debug(f'{1 + _} asteroid to be vaporized is at {asteroid}')
        angle_cleared = not len(asteroids_by_distance)
        if angle_cleared:
            polar_map.pop(scan_angle)
        scan_angle = next_scan_angle
    return asteroid


# Solver Methods ---------------------------------------------------------------


def solve(contents: set) -> int:
    """Solve puzzle part one

    :param contents: puzzle input contents
    :return: puzzle answer
    """
    detected_asteroids_map = map_detected_asteroids(asteroids=contents)
    answer = max(detected_asteroids_map.values())
    return answer


def solve_part_two(contents: map) -> int:
    """Solve puzzle part two

    :param contents: puzzle input contents
    :return: puzzle answer
    """
    detected_asteroids_map = map_detected_asteroids(asteroids=contents)
    max_asteroids = max(detected_asteroids_map.values())
    index = list(detected_asteroids_map.values()).index(max_asteroids)
    station = list(detected_asteroids_map.keys())[index]
    log.info(f'located {station=}')
    asteroids = contents - {station}
    x, y = vaporize(station=station, asteroids=asteroids, quantity=200)
    answer = x * 100 + y
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
        for map_ in load_contents(filename=args.filename):
            answer = solve(contents=map_)
            print(f'part one: answer: {answer}')
    if compute_part_two:
        for map_ in load_contents(filename=args.filename):
            answer = solve_part_two(contents=map_)
            print(f'part two: answer: {answer}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
