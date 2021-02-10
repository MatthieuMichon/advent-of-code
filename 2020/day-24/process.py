#!/usr/bin/env python

"""Advent of Code 2020

Day 24: Lobby Layout
"""

import itertools
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator

# Common -----------------------------------------------------------------------


DIRECTION_MAP = {
    'ne': '1', 'se': '3', 'sw': '4', 'nw': '6',
    'e': '2', 'w': '5',
}
ANGLES = [-30 + 60 * int(v) for v in sorted(DIRECTION_MAP.values())]

HEADING_COORDINATES = {
    30: (1, 1, 0),
    90: (0, 1, 1),
    150: (-1, 0, 1),
    210: (-1, -1, 0),
    270: (0, -1, -1),
    330: (1, 0, -1),
}


def read_paths(file: Path) -> list[list[int]]:
    """Read tile paths from a file

    :param file: file containing path directions
    :return: paths as a list of heading in degrees
    """
    paths = open(file).read()
    for d, v in DIRECTION_MAP.items():
        paths = paths.replace(d, v)
    paths = paths.split(os.linesep)
    paths = [[-30 + (int(s) * 60) for s in p] for p in paths if len(p)]
    return paths


def optimize(paths: list[list[int]]) -> list[list[int]]:
    """Optimize a list of paths

    :param paths: paths as a list of heading in degrees
    :return: optimized paths as a list of heading in degrees
    """
    paths = [Counter(p) for p in paths]
    optimized_paths = list()
    for path in paths:
        optimized_steps = list()
        for angle in ANGLES:
            if angle > 180:
                break
            distance = path[angle] - path[180 + angle]
            heading = angle if distance >= 0 else 180 + angle
            optimized_steps.extend([heading] * abs(distance))
        loop_sequence = set(30 + 120 * i for i in range(3))
        while all(angle in optimized_steps for angle in loop_sequence):
            for angle in loop_sequence:
                optimized_steps.remove(angle)
        loop_sequence = set(90 + 120 * i for i in range(3))
        while all(angle in optimized_steps for angle in loop_sequence):
            for angle in loop_sequence:
                optimized_steps.remove(angle)
        optimized_paths.append(optimized_steps)
    return optimized_paths


def transform(paths: list[list[int]]) -> Iterator[tuple[int]]:
    """Transform paths into destination tiles offsets

    :param paths: paths as a list of heading in degrees
    :return: lists of destination tiles offsets coordinates
    """
    for path in paths:
        coordinates = [0] * 3
        for step in path:
            offset_axis = HEADING_COORDINATES[step]
            for axis, offset_axis in enumerate(offset_axis):
                coordinates[axis] += offset_axis
        yield tuple(coordinates)


# Part One  --------------------------------------------------------------------


def print_part_one(inputs: list[Path]) -> None:
    """Print answer for part one

    :param inputs: list of puzzle input files
    :return: nothing
    """
    for file in inputs:
        paths = read_paths(file=file)
        tiles = list(transform(paths=paths))
        tiles = Counter(tiles)
        answer = len([t for t in tiles.values() if t % 2])
        print(f'Day 24 part one, file: {file}; answer: {answer}')


# Part Two  --------------------------------------------------------------------


ROUNDS = 100


def evolve(black_tiles: list[tuple[int]], rounds: int) -> list[tuple[int]]:
    """Evolve list of tails for a given number of rounds

    :param black_tiles: list of black tile coordinates
    :param rounds: number of evolutions
    :return: list of tile coordinates
    """
    def compute_area_ranges(tiles: list[tuple[int]]) -> list[range]:
        ranges: list[range] = list()
        axis_qty = len(tiles[0])
        for axis in range(axis_qty):
            values = [t[axis] for t in tiles]
            ranges.append(range(min(values), max(values)))
        return ranges

    def list_neighbors(position: tuple, tiles: list[tuple]) -> Iterator[tuple]:
        axis_qty = len(position)
        for offset in HEADING_COORDINATES.values():
            neighbor = tuple(position[axis] + offset[axis]
                             for axis in range(axis_qty))
            if neighbor in tiles:
                yield neighbor
    today = [t[0:2] for t in black_tiles]
    for round in range(rounds):
        area = compute_area_ranges(tiles=today)
        area_tiles = list(itertools.product(*area))
        for tile in area_tiles:
            neighbors = list_neighbors(position=tile, tiles=today)

        day = 1 + round
        if day < 10 or not(day % 10):
            print(f'Day {day}: {len(tiles)}')
    return tiles


def print_part_two(inputs: list[Path]) -> None:
    """Print answer for part two

    :param inputs: list of puzzle input files
    :return: nothing
    """
    for file in inputs:
        paths = read_paths(file=file)
        tiles = list(transform(paths=paths))
        tiles = Counter(tiles)
        black_tiles = [t for t, c in tiles.items() if c % 2]
        tiles = evolve(black_tiles=black_tiles, rounds=ROUNDS)
        answer = len(tiles)
        print(f'Day 24 part two, file: {file}; answer: {answer}')


# Common -----------------------------------------------------------------------


def main() -> int:
    """Main function

    :return: shell exit code
    """
    inputs = [
        #'test.txt',
        'example.txt',
        'input.txt'
    ]
    #print_part_one(inputs=[Path(i) for i in inputs])
    print_part_two(inputs=[Path(i) for i in inputs])
    return 0


if __name__ == '__main__':
    sys.exit(main())
