#!/usr/bin/env python
"""
Advent of Code 2020: Day 20
"""

import signal
import sys
import math
from pathlib import Path
from types import FrameType
import operator
import functools


DEBUG = False
SIDES = ('N', 'E', 'S', 'W')
MATCHING_CORNERS: tuple = (('E', 'S'), ('S', 'W'), ('W', 'N'), ('N', 'E'),)


# Common -----------------------------------------------------------------------


def rotate_corner_cw(corner: tuple) -> tuple:
    """
    Rotate a tuple of a variable amount of sides

    :param corner: tuple with number of sides
    :return: rotated quarter-turn clock-wise tuple
    """

    rotated_sides: list[str] = list()
    for s in corner:
        side_index = SIDES.index(s)
        next_index = (1 + side_index) % len(SIDES)
        rotated_sides.append(SIDES[next_index])
    return tuple(rotated_sides)


def flip_corner(corner: tuple) -> tuple:
    """
    Flip a tuple of a variable amount of sides

    :param corner: tuple with number of sides
    :return: flipped clock-wise tuple
    """

    fliped_sides: list[str] = list()
    for s in corner:
        if s == 'N':
            fliped_sides.append('W')
        elif s == 'E':
            fliped_sides.append('S')
        elif s == 'S':
            fliped_sides.append('E')
        elif s == 'W':
            fliped_sides.append('N')
    return tuple(fliped_sides)

# XX..
# X...
# ....
# ....

def flip(str_array: list[str]) -> list[str]:
    """
    Flip a list of strings on a top-left to bottom-right diagonal

    :param str_array: array as a list of strings
    :return: array flipped
    """

    flip_array = list(''.join(c) for c in zip(*str_array))
    return flip_array


def rotate_cw(str_array: list[str]) -> list[str]:
    """
    Rotate a list of strings quarter-turn clock-wise

    :param str_array: array as a list of strings
    :return: array rotated clock-wise
    """

    hflip_array = str_array[::-1]
    cw_rot_array = list(''.join(c) for c in zip(*hflip_array))
    return cw_rot_array


def rotate_ccw(str_array: list[str]) -> list[str]:
    """
    Rotate a list of strings quarter-turn counter-clock-wise

    :param str_array: array as a list of strings
    :return: array rotated counter clock-wise
    """

    zip_array = list(''.join(c) for c in zip(*str_array))
    ccw_rot_array = zip_array[::-1]
    return ccw_rot_array


class Tile:
    """
    Class for tracking internal states of a tile
    """

    def __init__(self, id_: int, rows: list[str]) -> None:
        """
        Initialize a new Tile instance

        :param id_: tile ID
        :param rows: tile contents
        """

        self.id = id_
        self.borders = dict()
        self.neighbors = {s: -1 for s in SIDES}
        # rows and cols start upper-left
        self.str_rows: list[str] = rows
        self.str_cols = list(''.join(c) for c in zip(*self.str_rows))
        self.compute_borders()

    def flip(self) -> None:
        """
        Rotate tile quarter-turn clock-wise

        :return: nothing
        """

        self.str_rows = flip(str_array=self.str_rows)
        self.str_cols = list(''.join(c) for c in zip(*self.str_rows))
        self.compute_borders()
        self.neighbors = {s: -1 for s in SIDES}

    def rotate_cw(self) -> None:
        """
        Rotate tile quarter-turn clock-wise

        :return: nothing
        """

        self.str_rows = rotate_cw(str_array=self.str_rows)
        self.str_cols = list(''.join(c) for c in zip(*self.str_rows))
        self.compute_borders()
        self.neighbors = {s: -1 for s in SIDES}

    def rotate_ccw(self) -> None:
        """
        Rotate internal string array a quarter-turn counter-clock wise

        :return: nothing
        """

        self.str_rows = rotate_ccw(str_array=self.str_rows)
        self.str_cols = list(''.join(c) for c in zip(*self.str_rows))
        self.compute_borders()
        self.neighbors = {s: -1 for s in SIDES}

    def compute_borders(self) -> None:
        """
        Compute borders data

        :return: nothing
        """

        str_array = self.str_rows.copy()
        for side in SIDES:
            self.borders[side] = str_array[0]
            self.borders[side + '_inv'] = str_array[0][::-1]
            str_array = rotate_ccw(str_array=str_array)

    def search_neighbors(self, tiles_by_id: dict[int, any]):
        """
        Search neighbors of the current tile

        :param tiles_by_id: Tiles instances per ID
        :return: nothing
        """

        opposite_tiles = tiles_by_id.copy()
        opposite_tiles.pop(self.id)
        for side in SIDES:
            matches = list()
            border = self.borders[side]

            for op_tile in opposite_tiles.values():
                for op_side, op_border in op_tile.borders.items():
                    if border == op_border:
                        matches.append([op_tile.id, op_side, op_border])
            if matches:
                self.neighbors[side] = matches
            else:
                self.neighbors[side] = None


def read_tiles(file: Path) -> dict[int, Tile]:
    """
    Read tiles from a given file

    :param file: file containing the input values
    :return: Tiles instances per ID
    """

    tiles = dict()
    str_array = list()
    id_:int = -1
    for line in open(file):
        if 'Tile ' in line:
            id_=int(line[5:-2])
        elif len(line) > 2:
            str_array.append(line.strip())
            last_row = len(str_array) == len(line.strip())
            if last_row:
                tiles[id_] = Tile(id_=id_, rows=str_array)
                str_array = list()

    return tiles


# def load_tiles(file: Path) -> Iterator[dict]:
#     """
#     Load tiles data from a given file
#
#     :param file: file containing the input values
#     :return: tile iterator
#     """
#
#     tile = dict()
#     for line in open(file):
#         if 'Tile ' in line:
#             tile['id'] = int(line[5:-2])
#             tile['rows'] = list()
#         elif len(line) > 2:
#             tile['rows'].append(line.strip())
#             last_row = len(tile['rows']) == len(line.strip())
#             if last_row:
#                 yield tile
#                 tile = dict()


# Part One ---------------------------------------------------------------------


def compute_borders(tile: Tile) -> dict[str, any]:
    """
    Compute possible borders for all tiles in the tile map

    :param tile: Tile instance
    :return: per-tile data with added border data
    """

    rows = tile.str_rows
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

    raw_tiles = read_tiles(file=file)
    border_map = {k: compute_borders(tile=v) for k, v in raw_tiles.items()}

    return border_map


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


def compute_matches(tiles_by_id: dict[int, Tile]) -> dict[int, dict]:
    """
    Match borders with identical hash values between any pair of tiles

    :param tiles_by_id: Tiles instances per ID
    :return: matches per tile ID
    """

    matches_per_tile = dict()
    for tile in tiles_by_id.values():
        matching_borders = dict()
        opposite_tiles = tiles_by_id.copy()
        opposite_tiles.pop(tile.id)
        for side in SIDES:
            matches = list()
            border = tile.borders[side]

            for op_tile in opposite_tiles.values():
                for op_side, op_border in op_tile.borders.items():
                    if border == op_border:
                        matches.append([op_tile.id, op_side, op_border])
            if matches:
                matching_borders[side] = matches
        if matching_borders:
            matches_per_tile[tile.id] = matching_borders

    return matches_per_tile


#def transform_tile(matches: dict, constraints: dict[str, any]) -> dict


def arrange_tiles(tiles_by_id: dict[int, Tile],
                  matches_by_id: dict[int, dict]) -> list[list[int]]:
    """
    Arrange adjacent tiles

    :param tiles_by_id: matches per tile ID
    :param matches_by_id: matches per tile ID
    :return: 2d list of tile IDs
    """

    image_width = math.sqrt((len(tiles_by_id)))
    assert image_width.is_integer()
    image_width = int(image_width)
    board = dict()

    corner_tiles = tuple(
        tiles_by_id[id_] for id_, sides in matches_by_id.items()
        if len(sides) == 2)

    seed_tile = corner_tiles[0]
    req_neighbors = MATCHING_CORNERS[0]
    actual_corners = tuple(matches_by_id[seed_tile.id].keys())
    while req_neighbors != actual_corners:
        seed_tile.rotate_cw()
        seed_tile.search_neighbors(tiles_by_id=tiles_by_id)
        actual_corners = rotate_corner_cw(actual_corners)
    board[(0, 0)] = seed_tile

    for i in range(1, image_width):
        last_tile: Tile = board[(0, i - 1)]
        tile: Tile = tiles_by_id[last_tile.neighbors['E'][0][0]]
        flip_required = 'inv' in last_tile.neighbors['E'][0][1]
        if flip_required:
            tile.flip()
            tile.search_neighbors(tiles_by_id=tiles_by_id)
            actual_corners = flip_corner(corner=actual_corners)
        req_neighbors = ('E', 'S', 'W')
        actual_corners = tuple(matches_by_id[tile.id].keys())
        while req_neighbors != actual_corners:
            tile.rotate_cw()
            tile.search_neighbors(tiles_by_id=tiles_by_id)
            actual_corners = rotate_corner_cw(actual_corners)
        board[(0, i)] = tile

    #
    # for i, tile in enumerate(corners):
    #     orientation: int = i
    #     req_corners = MATCHING_CORNERS[orientation]
    #     actual_corners = tuple(matches_by_id[tile.id].keys())
    #     while req_corners != actual_corners:
    #         tile.str_rows = Tile.rotate_cw(tile.str_rows)
    #         tile.borders = Tile.compute_borders(tile.str_rows)
    #         orientation = (1 + orientation) % 4
    #         actual_corners = rotate_corner_cw(actual_corners)
    #     if i == 0:
    #         board[(0, 0)] = tile
    #     if i == 1:
    #         board[(0, image_width - 1)] = tile
    #     if i == 2:
    #         board[(image_width - 1, image_width - 1)] = tile
    #     if i == 3:
    #         board[(image_width - 1, 0)] = tile

    return [[0]]

# def chop_borders(tile: list[str]) -> list[str]:
#     """
#     Chop borders from a tile
#
#     :param tile: binary string bitmap
#     :return: binary string bitmap
#     """
#
#     tile_chopped_n_s = tile[1:-1]
#     rot_cw = list(''.join(c) for c in zip(*tile_chopped_n_s[::-1]))
#     tile_rot_chopped_n_s_e_w = rot_cw[1:-1]
#     tile_chopped_n_s_e_w = list(
#         ''.join(c) for c in zip(*tile_rot_chopped_n_s_e_w))[::-1]
#
#     return tile_chopped_n_s_e_w
#
#
# def form_image(tiles: list[list[str]]) -> list[str]:
#     """
#     Form an image from a list of tiles after removing all borders
#
#     :param tiles: list of tiles
#     :return: binary string bitmap
#     """
#
#     chopped_tiles = [chop_borders(t) for t in tiles]
#
#     return ['a']
#
#
# def list_operations(
#         tile: dict, outer_borders: set, neighbors: dict[int, dict]) -> list:
#     """
#     List operations required on a tile for matching a set of constraints
#
#     :param tile:
#     :param outer_borders:
#     :param neighbors:
#     :return:
#     """
#
#     borders = next(iter(tile.values()))
#
#     #current_inner_borders = {v for v in tile.values()}
#
#     return None
#
#
# def assemble(tile_borders: dict[int, dict], tile_matches: dict[int, dict]) -> list[str]:
#     """
#     Assemble an image by transforming tiles
#
#     :param tile_borders: mapping of all tile borders
#     :param tile_matches: mapping of all possible tile matches
#     :return: binary string image
#     """
#
#     corner_tiles = [{k: v} for k, v in tile_matches.items() if len(v) == 2]
#     assert len(corner_tiles) == 4
#
#     list_operations(tile=corner_tiles[0], outer_borders={'E', 'N'}, neighbors=dict())
#
#     print(corner_tiles)
#
#     return ['hello']


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    tiles_by_id = read_tiles(file=file)
    matches_by_id = compute_matches(tiles_by_id=tiles_by_id)
    tiles_by_id = arrange_tiles(tiles_by_id=tiles_by_id, matches_by_id=matches_by_id)

    corner_tiles = {tiles_by_id[i] for i, m in matches_by_id.items() if len(m.values()) == 2}
    outer_tiles = {tiles_by_id[i] for i, m in matches_by_id.items() if len(m.values()) == 3}
    for id_, tile in tiles_by_id.items():
        b = compute_borders(tile=tile)
    tiles_by_id = read_tiles(file=file)

    print(len(list(tiles_by_id)))

    #
    # border_map = decode(file=file)
    # tile_matches = match_borders(border_map=border_map)
    # image = assemble(tile_borders=border_map, tile_matches=tile_matches)

    print(0)


# Main -------------------------------------------------------------------------


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    #files = ['./example.txt', './input.txt']
    #files = ['./input.txt']
    files = []
    for f in files:
        print(f'In file {f}:')
        print(f'\tPart One: {process(file=Path(f))}')

    files = ['./example.txt', './input.txt']
    #files = ['./input.txt']
    #files = []
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
