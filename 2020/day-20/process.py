#!/usr/bin/env python
"""
Advent of Code 2020: Day 20
"""

import signal
import sys
import itertools
from pathlib import Path
from types import FrameType
import operator
import functools


DEBUG = False
SIDES = ('N', 'E', 'S', 'W')
MATCHING_CORNERS: tuple = (('E', 'S'), ('S', 'W'), ('W', 'N'), ('N', 'E'),)

AXIS_QTY = 2
OFFSETS = [(-1, 0, +1)] * AXIS_QTY
POSITIONS = list(itertools.product(*OFFSETS))
SELF_POS = tuple([0 for _ in range(AXIS_QTY)])
NEIGHBOR_OFFSETS = {p for p in POSITIONS if p != SELF_POS and abs(sum(p)) == 1}


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
    return list(reversed(str_array.copy()))


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


def compute_transformations(str_array: list[str]) -> list[list[str]]:
    """
    Compute all possible transformations

    :param str_array: array as a list of strings
    :return: possible transformations
    """

    str_array_cw90 = rotate_cw(str_array=str_array)
    str_array_cw180 = rotate_cw(str_array=str_array_cw90)
    str_array_cw270 = rotate_cw(str_array=str_array_cw180)
    transformations = [
        str_array, str_array_cw90, str_array_cw180, str_array_cw270,
        flip(str_array), flip(str_array_cw90), flip(str_array_cw180),
        flip(str_array_cw270),
    ]

    return transformations


def arrange_tiles(tile_map: dict[int, any]):
    """
    Flip and rotate tiles until inner borders match

    :param tile_map: map of tiles per ID
    :return: array of tuple of tile ID and required transformation
    """

    n = int(len(tile_map) ** 0.5)
    assembled = [[(0, 0)] * n for _ in range(n)]
    remaining = set(tile_map.keys())

    def arrange_tile(tile_rank: int) -> bool:
        if tile_rank == n * n:
            return True
        row = tile_rank // n
        col = tile_rank % n
        for id_ in list(remaining):
            for i, transformation in enumerate(tile_map[id_]):
                up_ok = left_ok = True
                if row > 0:
                    up_tileid, up_transformation = assembled[row - 1][col]
                    up_tile = tile_map[up_tileid][up_transformation]
                    up_ok = all(transformation[0][i] == up_tile[9][i] for i in range(10))
                if col > 0:
                    left_tileid, left_transformation = assembled[row][col - 1]
                    left_tile = tile_map[left_tileid][left_transformation]
                    left_ok = all(transformation[i][0] == left_tile[i][9] for i in range(10))
                if up_ok and left_ok:
                    assembled[row][col] = (id_, i)
                    remaining.remove(id_)
                    if arrange_tile(tile_rank=tile_rank + 1):
                        return True
                    remaining.add(id_)
        return False

    arrange_tile(tile_rank=0)

    return assembled


# def compute_matches(tiles_by_id: dict[int, Tile]) -> dict[int, dict]:
#     """
#     Match borders with identical hash values between any pair of tiles
#
#     :param tiles_by_id: Tiles instances per ID
#     :return: matches per tile ID
#     """
#
#     matches_per_tile = dict()
#     for tile in tiles_by_id.values():
#         matching_borders = dict()
#         opposite_tiles = tiles_by_id.copy()
#         opposite_tiles.pop(tile.id)
#         for side in SIDES:
#             matches = list()
#             border = tile.borders[side]
#
#             for op_tile in opposite_tiles.values():
#                 for op_side, op_border in op_tile.borders.items():
#                     if border == op_border:
#                         matches.append([op_tile.id, op_side, op_border])
#             if matches:
#                 matching_borders[side] = matches
#         if matching_borders:
#             matches_per_tile[tile.id] = matching_borders
#
#     return matches_per_tile
#
#
# def arrange_tiles_try1(tiles_by_id: dict[int, Tile],
#                   matches_by_id: dict[int, dict]) -> list[list[int]]:
#     """
#     Arrange adjacent tiles
#
#     :param tiles_by_id: matches per tile ID
#     :param matches_by_id: matches per tile ID
#     :return: 2d list of tile IDs
#     """
#
#     image_width = math.sqrt((len(tiles_by_id)))
#     assert image_width.is_integer()
#     image_width = int(image_width)
#     board = dict()
#
#     corner_tiles = tuple(
#         tiles_by_id[id_] for id_, sides in matches_by_id.items()
#         if len(sides) == 2)
#
#     tile = None
#     for row_index in range(image_width):
#         for col_index in range(image_width):
#             start_tile = (row_index == 0) and (col_index == 0)
#             if start_tile:
#                 tile = corner_tiles[0]
#                 req_neighbors = MATCHING_CORNERS[0]
#                 actual_corners = tuple(matches_by_id[tile.id].keys())
#                 while req_neighbors != actual_corners:
#                     tile.rotate_cw()
#                     tile.search_neighbors(tiles_by_id=tiles_by_id)
#                     actual_corners = rotate_corner_cw(actual_corners)
#                 board[(row_index, col_index)] = tile
#             else:
#                 if col_index > 0:
#                     assert tile
#                     last_tile: Tile = tile
#                     tile = tiles_by_id[last_tile.neighbors['E'][0][0]]
#                     tile.search_neighbors(tiles_by_id=tiles_by_id)
#                     actual_corners = tuple(matches_by_id[tile.id].keys())
#                     flip_required = 'inv' in last_tile.neighbors['E'][0][1]
#                     if flip_required:
#                         tile.flip()
#                         tile.search_neighbors(tiles_by_id=tiles_by_id)
#                         actual_corners = flip_corner(corner=actual_corners)
#                     while not tile.neighbors['W'] or tile.neighbors['W'][0][0] != last_tile.id:
#                         tile.rotate_cw()
#                         tile.search_neighbors(tiles_by_id=tiles_by_id)
#                         actual_corners = rotate_corner_cw(actual_corners)
#                     board[(row_index, col_index)] = tile
#                 else:
#                     assert col_index == 0
#                     assert row_index > 0
#                     last_tile: Tile = board[(row_index - 1), col_index]
#                     tile = tiles_by_id[last_tile.neighbors['S'][0][0]]
#                     tile.search_neighbors(tiles_by_id=tiles_by_id)
#                     actual_corners = tuple(matches_by_id[tile.id].keys())
#                     flip_required = 'inv' in last_tile.neighbors['S'][0][1]
#                     if flip_required:
#                         tile.flip()
#                         tile.search_neighbors(tiles_by_id=tiles_by_id)
#                         actual_corners = flip_corner(corner=actual_corners)
#                     while not tile.neighbors['N'] or tile.neighbors['N'][0][0] != last_tile.id:
#                         tile.rotate_cw()
#                         tile.search_neighbors(tiles_by_id=tiles_by_id)
#                         actual_corners = rotate_corner_cw(actual_corners)
#                     board[(row_index, col_index)] = tile
#         print(0)
#
#     return [[0]]
#
#
# def list_neighbors(
#         tile_map: dict[tuple[int, int], int],
#         position: tuple[int, int]) -> set[int]:
#     """
#     List neighbors
#
#     :param tile_map: tile IDs per position
#     :param position: coordinates
#     :return: set of IDs
#     """
#
#     neighbors = list()
#     npos = [(position[0] + o[0], position[1] + o[1]) for o in NEIGHBOR_OFFSETS]
#     for pos in npos:
#         if pos not in tile_map:
#             continue
#         neighbors.append(tile_map[pos])
#
#     return set(neighbors)
#
#
# def place_tiles(tile_matches: dict[int, dict[str, dict]]) -> dict[tuple, int]:
#     """
#     Place tiles according to a map
#
#     :param tile_matches: tile matches by tile id
#     :return: TBD
#     """
#
#     neighbor_map = {
#         k: [vv[0][0] for vv in v.values()]
#         for k, v in tile_matches.items()}
#     neighbor_map_copy = neighbor_map.copy()
#
#     tiles_qty = len(neighbor_map)
#     assert math.sqrt(tiles_qty).is_integer()
#     image_width = int(math.sqrt(tiles_qty))
#
#     corner_tiles = tuple(
#         id_ for id_, sides in tile_matches.items() if len(sides) == 2)
#     border_tiles = tuple(
#         id_ for id_, sides in tile_matches.items() if len(sides) <= 3)
#
#     tile_map = dict()
#     tile_map[(0, 0)] = corner_tiles[0]
#     last_tile = corner_tiles[0]
#
#     for col in range(1, image_width):
#         last_tile_neighbors = neighbor_map[last_tile]
#         tiles = set(border_tiles) & set(last_tile_neighbors) - set(tile_map.values())
#         tile = list(tiles)[0]
#         neighbor_map.pop(last_tile)
#         assert tile not in tile_map.values()
#         tile_map[(col, 0)] = tile
#         last_tile = tile
#
#     for row in range(1, image_width):
#         last_tile_neighbors = neighbor_map[last_tile]
#         tiles = set(border_tiles) & set(last_tile_neighbors) - set(tile_map.values())
#         tile = list(tiles)[0]
#         neighbor_map.pop(last_tile)
#         assert tile not in tile_map.values()
#         tile_map[(image_width - 1), row] = tile
#         last_tile = tile
#
#     for col in reversed(range(0, image_width - 1)):
#         last_tile_neighbors = neighbor_map[last_tile]
#         tiles = set(border_tiles) & set(last_tile_neighbors) - set(tile_map.values())
#         tile = list(tiles)[0]
#         neighbor_map.pop(last_tile)
#         assert tile not in tile_map.values()
#         tile_map[col, (image_width - 1)] = tile
#         last_tile = tile
#
#     for row in reversed(range(1, image_width - 1)):
#         last_tile_neighbors = neighbor_map[last_tile]
#         tiles = set(border_tiles) & set(last_tile_neighbors) - set(tile_map.values())
#         tile = list(tiles)[0]
#         neighbor_map.pop(last_tile)
#         assert tile not in tile_map.values()
#         tile_map[(0, row)] = tile
#         last_tile = tile
#
#     neighbor_map.pop(last_tile)
#
#     # scan over all map tiles
#
#     for row in range(1, image_width - 1):
#         for col in range(1, image_width - 1):
#             candidates = list()
#             neighbor_id_list = list_neighbors(tile_map=tile_map, position=(col, row))
#             for nid in neighbor_id_list:
#                 candidates.append(neighbor_map_copy[nid])
#             tile = set.intersection(*map(set, candidates)) - set(tile_map.values())
#             assert len(tile) == 1
#             tile = list(tile)[0]
#             tile_map[(col, row)] = tile
#             neighbor_map.pop(tile)
#
#     return tile_map
#
#
# def arrange_tiles(tile_map: dict[tuple[int, int], int], tiles_by_id: dict[int, Tile]):
#
#     tiles_qty = len(tile_map)
#     assert math.sqrt(tiles_qty).is_integer()
#     image_width = int(math.sqrt(tiles_qty))
#
#     for row in range(image_width):
#         for col in range(image_width):
#             if (col, row) == (0, 0):
#                 continue
#             match_left_tile = col > 0
#             match_upper_tile = (col == 0) and (row > 0)
#
#             if match_left_tile:
#                 left_tile_pos = (col - 1, row)
#                 left_tile = tile_map[left_tile_pos]
#                 opposite_border = tiles_by_id[left_tile].borders['E']
#                 tile = tiles_by_id[tile_map[(col, row)]]
#                 print(0)


def assemble_tiles(tiles_by_id: dict[int, Tile], tile_map: list[list[tuple]]
                   ) -> list[list[str]]:
    """
    Assemble tiles

    :param tiles_by_id: tile instances by ID
    :param tile_map: array of tuple of tile ID and required transformation
    :return: list of strings
    """

    tile_size = len(list(tiles_by_id.values())[0].str_rows[0])
    horiz_tiles = int(len(tiles_by_id) ** 0.5)
    image_size = horiz_tiles * tile_size
    image = [[' '] * image_size for _ in range(image_size)]

    for i, row in enumerate(tile_map):
        for j, tile_data in enumerate(row):
            row_slice = [j * tile_size, (j + 1) * tile_size]
            id = tile_data[0]
            transform = tile_data[1]
            flip = transform // 4
            rotations = transform % 4
            for _ in range(rotations):
                tiles_by_id[id].rotate_cw()
            if flip:
                tiles_by_id[id].flip()
            for line in range(tile_size):
                image_row = i * tile_size + line
                image[image_row][slice(*row_slice)] = tiles_by_id[id].str_rows[line]

    return image


def remove_borders(image: list[list[str]], size: int) -> list[list[str]]:
    """
    Remove borders of the given image

    :param image: 2d list of strings
    :param size: individual tile width
    :return: 2d list of strings
    """

    cropped_list = list()
    is_border = lambda i: (i % size) in [0, 9]
    for i, row in enumerate(image):
        if is_border(i):
            continue
        cropped_row = list()
        for j, cell in enumerate(row):
            if is_border(j):
                continue
            cropped_row.append(cell)
        cropped_list.append(cropped_row)

    return cropped_list


def correlate(a: list[list[str]], b: list[list[str]]) -> bool:
    """
    Correlate two patterns

    :param a: 2d list of strings
    :param b: 2d list of strings
    :return: True if argument match
    """

    int_ = lambda l: int(''.join(l.replace('#', '1').replace(' ', '0').replace('.', '0')), 2)

    a_int_array = [int_(''.join(l)) for l in a]
    b_int_array = [int_(''.join(l)) for l in b]
    assert len(a_int_array) == len(b_int_array)

    for i, a_int in enumerate(a_int_array):
        b_int = b_int_array[i]
        c = a_int & b_int
        if c != c | b_int:
            return False

    return True


img = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###""".split('\n')


def search_pattern(image: list[list[str]], pattern: list[list[str]]
                   ) -> list[list[str]]:
    """
    Search for a pattern in the given image

    :param image: 2d list of strings
    :param pattern: 2d list of strings
    :return: 2d list of strings
    """

    image = [''.join(r) for r in image]
    image_size = len(image)
    pattern_hsize = len(pattern[0])
    pattern_vsize = len(pattern)
    tries = 0

    for transform in range(8):
        #assert img != image
        for i in range(image_size - pattern_vsize):
            v_crop = image[i:i + pattern_vsize]
            for j in range(image_size - pattern_hsize):
                crop = [r[j:j + pattern_hsize] for r in v_crop]
                c = correlate(a=crop, b=pattern)
                tries += 1
                if c:
                    print(crop)
        do_flip = transform == 4
        if not do_flip:
            image = rotate_cw(image)
        else:
            image = flip(image)

        print(tries)
    print(tries)


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    tiles_by_id = read_tiles(file=file)
    tile_transforms = {tile.id: compute_transformations(tile.str_rows) for tile in tiles_by_id.values()}
    tile_map = arrange_tiles(tile_map=tile_transforms)
    image = assemble_tiles(tiles_by_id=tiles_by_id, tile_map=tile_map)
    image = remove_borders(image=image, size=10)

    pattern = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ']
    image = search_pattern(image=image, pattern=pattern)

    return 0


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
    files = ['./example.txt']
    files = ['./input.txt']
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
