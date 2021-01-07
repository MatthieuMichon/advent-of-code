#!/usr/bin/env python
"""
Advent of Code 2020: Day 20
"""

import signal
import sys
from pathlib import Path
from types import FrameType
from typing import Iterator
import operator
import functools


DEBUG = False
SIDES = ['N', 'S', 'E', 'W']


# Common -----------------------------------------------------------------------


def load_tiles(file: Path) -> Iterator[dict]:
    """
    Load tiles data from a given file

    :param file: file containing the input values
    :return: tile iterator
    """

    tile = dict()
    for line in open(file):
        if 'Tile ' in line:
            tile['id'] = int(line[5:-2])
            tile['rows'] = list()
        elif len(line) > 2:
            tile['rows'].append(line.strip())
            last_row = len(tile['rows']) == len(line.strip())
            if last_row:
                yield tile
                tile = dict()


def compute_borders(tile: dict[str, any]) -> dict[str, any]:
    """
    Compute possible borders for all tiles in the tile map

    :param tile_map: per-tile data
    :return: per-tile data with added border data
    """

    rows = tile['rows']
    rot_cw = list(''.join(c) for c in zip(*rows[::-1]))

    raw = dict()
    raw['N'] = rows[0]
    raw['S'] = rows[-1]
    raw['E'] = rot_cw[-1][::-1]
    raw['W'] = rot_cw[0][::-1]
    raw['list'] = [s for s in raw.values()]

    conv = lambda l: int(''.join(l.replace('#', '1').replace('.', '0')), 2)
    int_ = {k: conv(v) for k, v in raw.items() if len(k) == 1}
    int_['list'] = [s for s in int_.values()]

    rev = lambda i: int(f'{i:010b}'[::-1], 2)
    rev_int = {k: rev(v) for k, v in int_.items() if len(k) == 1}
    rev_int['list'] = [s for s in rev_int.values()]

    # associative hash for matching borders if tile is flipped
    hash_ = lambda v, i, r: 2**20 * (i[v] & r[v]) + 2**10 * (i[v] ^ r[v]) + (i[v] | r[v])
    id_ = {k: hash_(k, int_, rev_int) for k, v in int_.items() if len(k) == 1}
    id_['list'] = [s for s in id_.values()]

    borders = {
        'id': id_,
        'raw': raw,
        'int': int_,
        'rev_int': rev_int
    }

    return borders


def match_borders(border_map: dict[int, any]) -> dict[int, dict]:
    """
    Match borders with identical hash values between any pair of tiles

    :param border_map:
    :return: TODO
    """

    matches_per_tile = dict()
    for k, v in border_map.items():
        matches = dict()
        border_id_list = [v['int'][kk] for kk in SIDES]
        for kk, vv in border_map.items():
            if kk == k:
                continue
            opposite_id_list = [vv['int'][s] for s in SIDES] + [vv['rev_int'][s] for s in SIDES]
            if not set(border_id_list) & set(opposite_id_list):
                continue
            for i, vvv in enumerate(border_id_list):
                for ii, vvvv in enumerate(opposite_id_list):
                    if vvv == vvvv:
                        if DEBUG:
                            print(f"matched tile #{k} side {SIDES[i]} with tile #{kk} side {['N', 'S', 'E', 'W'][ii % 4]}")
                        matches[SIDES[i]] = [kk, SIDES[ii % 4]]
        matches_per_tile[k] = matches

    return matches_per_tile


def decode(file: Path) -> any:
    """
    Decode contents of the given file

    :param file: file containing the input values
    :return: tile iterator
    """

    raw_tiles = load_tiles(file=file)
    border_map = {t['id']: compute_borders(tile=t) for t in raw_tiles}

    return border_map

# Part One ---------------------------------------------------------------------


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    border_map = decode(file=file)
    matched_tiles = match_borders(border_map=border_map)
    corner_tiles = [k for k, v in matched_tiles.items() if len(v) == 2]
    corners_id_product = functools.reduce(operator.mul, corner_tiles)
    return corners_id_product


# Part Two ---------------------------------------------------------------------


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    corners_id_product = 0
    return corners_id_product


# Main -------------------------------------------------------------------------


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    files = ['./example.txt', './input.txt']
    #files = ['./input.txt']
    #files = []
    for f in files:
        print(f'In file {f}:')
        print(f'\tPart One: {process(file=Path(f))}')

    files = ['./example_part2.txt', './input.txt']
    #files = ['./input.txt']
    files = []
    for f in files:
        print(f'In file {f}:')
        print(f'\tPart Two: {process_part2(file=Path(f))}')

    return 0


def handle_sigint(signal_value: signal.Signals, frame: FrameType) -> None:
    """
    Interrupt signal call-back method

    :param signal_value: signal (expected SIGINT)
    :param frame: current stack frame at the time of signal
    :return: nothing
    """

    assert signal_value == signal.SIGINT
    print(frame.f_locals)
    sys.exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    sys.exit(main())
