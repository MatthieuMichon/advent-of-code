#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day Three
Puzzle Solution in Python
"""

import argparse
import logging
import operator
import os
import sys
from typing import Iterator

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def convert_token(token: str) -> tuple[int, int]:
    """Converts string token into 2d grid offset

    :param token: token in string format
    :return: 2d grid offset in integer format
    """
    direction, length = token[:1], int(token[1:])
    assert direction in ['R', 'L', 'U', 'D']
    if direction in ['L', 'D']:
        length *= -1
    offset = (length, 0) if direction in ['R', 'L'] else (0, length)
    return offset


def load_contents(filename: str) -> list[list[tuple[int, int]]]:
    """Load contents from the given file

    :param filename: filename as string
    :return: converted contents
    """
    wires = list(open(filename).read().strip().split(os.linesep))
    log.info(f'Loaded {len(wires)} wires from {filename}')
    assert 0 == len(wires) % 2
    contents = [[convert_token(t) for t in w.split(',')] for w in wires]
    return contents


def enumerate_corners(wire: list[tuple[int, int]]) -> Iterator[tuple[int, int]]:
    """Enumerate corners for the given wire path

    :param wire: list of segments for a given wire
    :yield: location of segment corner
    """
    corner = (0, 0)
    for offset in wire:
        corner = tuple(map(operator.add, corner, offset))
        yield corner


def enumerate_segments(wire: list[tuple[int, int]]) \
        -> Iterator[tuple[tuple[int, int]]]:
    """Enumerates segments out of a given wire path

    :param wire: list of segments for a given wire
    :yield: segments extremities
    """
    last_corner = (0, 0)
    for offset in wire:
        corner = tuple(map(operator.add, last_corner, offset))
        yield tuple([last_corner, corner])
        last_corner = corner


def measure_distance(segment: tuple[tuple[int, int]]) -> float:
    """

    :param segment:
    :return:
    """
    a, b = segment[0:2]
    px = b[0] - a[0]
    py = b[1] - a[1]
    norm = px * px + py * py
    u = (-a[0] * px - a[1] * py) / float(norm)
    u = min(1, max(u, 0))
    x = a[0] + u * px
    y = a[1] + u * py
    dist = (x * x + y * y)
    return dist


def measure_manhattan_distance(segment: tuple[tuple[int, int]]) -> int:
    """Measure the manhattan distance between a segment and the central port

    :param segment: pair of coordinates
    :return: manhattan distance
    """
    a, b = segment[0:2]
    if a[0] == b[0]:
        distance = abs(a[0])
        if (a[1] < 0) != (b[1] < 0): # different sign
            return distance
        else:
            distance += abs(min([a[1], b[1]]))
            return distance
    else:
        distance = abs(a[1])
        if (a[0] < 0) != (b[0] < 0): # different sign
            return distance
        else:
            distance += abs(min([a[0], b[0]]))
            return distance


def sort_closest_central(segments: list[tuple[tuple[int, int]]]) \
        -> list[tuple[tuple[int, int]]]:
    """Sort segments with the ones that are closest to the central port first

    :param segments: list of segments with extremities points
    :return: sorted list of segments with extremities points
    """
    sorted_segments = sorted(
        segments, key=lambda s: measure_manhattan_distance(s))
    return sorted_segments


def intersects(segments: tuple[tuple[tuple[int, int]]]) -> bool:
    """Test if the given segments intersect

    :param segments: pair of segments
    :return: true if both segments intersect
    """

    if min([segments[0][0][0], segments[0][1][0]]) >= \
            max([segments[1][0][0], segments[1][1][0]]):
        return False
    if max([segments[0][0][0], segments[0][1][0]]) <= \
            min([segments[1][0][0], segments[1][1][0]]):
        return False
    if min([segments[0][0][1], segments[0][1][1]]) >= \
            max([segments[1][0][1], segments[1][1][1]]):
        return False
    if max([segments[0][0][1], segments[0][1][1]]) <= \
            min([segments[1][0][1], segments[1][1][1]]):
        return False
    return True


def intersect_location(segments: tuple[tuple[tuple[int, int]]]) \
        -> tuple[int, int]:
    """Return the location where segments intersect

    :param segments: pair of segments
    :return: true if both segments intersect
    """
    if segments[0][0][0] == segments[0][1][0]:
        return segments[0][0][0], segments[1][0][1]
    else:
        return segments[1][0][0], segments[0][0][1]


def crosses(segment: tuple[tuple[int, int]], location: tuple[int, int]) -> bool:
    """Check if a segment crosses a location

    :param segment: segment
    :param location: grid coordinates
    :return: true if the location is on the segment
    """
    x, y = location
    ax, ay = segment[0]
    bx, by = segment[1]
    if ax == bx == x and min(ay, by) < y < max(ay, by):
        return True
    if ay == by == y and min(ax, bx) < x < max(ax, bx):
        return True
    return False


# Solving Methods --------------------------------------------------------------


def solve(contents: list[list[tuple[int, int]]]) -> int:
    """Solve the first part of the puzzle

    :param contents: list of offsets per wire
    :return: answer of the puzzle
    """
    segments_by_orientation = {
        'horizontal': [],
        'vertical': []
    }
    for wire in contents[0:2]:
        segments = list(enumerate_segments(wire=wire))
        even_segments = [s for i, s in enumerate(segments) if 0 == i % 2]
        odd_segments = [s for i, s in enumerate(segments) if 1 == i % 2]
        even_are_vertical = even_segments[0][0][0] == even_segments[0][1][0]
        horizontal = odd_segments if even_are_vertical else even_segments
        vertical = even_segments if even_are_vertical else odd_segments
        segments_by_orientation['horizontal'].append(horizontal)
        segments_by_orientation['vertical'].append(vertical)
    intersection_distances = []
    for i, hgroud in enumerate(segments_by_orientation['horizontal']):
        for sh in hgroud:
            vgroup = segments_by_orientation['vertical'][1 - i]
            for sv in vgroup:
                if intersects((sh, sv)):
                    intersection_distances.append(
                        sum(map(abs, intersect_location((sh, sv)))))
                    log.debug('intersect: '
                              f'{intersect_location((sh, sv))}, {sh}, {sv}')
    answer = min(intersection_distances)
    return answer


def solve_part_two(contents: list[list[tuple[int, int]]]) -> int:
    """Solve the second part of the puzzle

    :param contents: list of offsets per wire
    :return: answer of the puzzle
    """
    segments_by_orientation = {
        'horizontal': [],
        'vertical': []
    }
    for wire in contents[0:2]:
        segments = list(enumerate_segments(wire=wire))
        even_segments = [s for i, s in enumerate(segments) if 0 == i % 2]
        odd_segments = [s for i, s in enumerate(segments) if 1 == i % 2]
        even_are_vertical = even_segments[0][0][0] == even_segments[0][1][0]
        horizontal = odd_segments if even_are_vertical else even_segments
        vertical = even_segments if even_are_vertical else odd_segments
        segments_by_orientation['horizontal'].append(horizontal)
        segments_by_orientation['vertical'].append(vertical)
    intersection_locations = []
    for i, hgroud in enumerate(segments_by_orientation['horizontal']):
        for sh in hgroud:
            vgroup = segments_by_orientation['vertical'][1 - i]
            for sv in vgroup:
                if intersects((sh, sv)):
                    intersection_locations.append(intersect_location((sh, sv)))
                    log.debug('intersect: '
                              f'{intersect_location((sh, sv))}, {sh}, {sv}')
    log.debug(f'Found {len(intersection_locations)} intersections')
    answer = -1
    return answer


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = ('%(asctime)s - %(levelname)s - %(module)s - '
              '%(funcName)s - %(message)s')


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
        print(answer)
    if compute_part_two:
        contents = load_contents(filename=args.filename)
        answer = solve_part_two(contents=contents)
        print(answer)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
