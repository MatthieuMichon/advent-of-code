#!/usr/bin/env python
"""
Advent of Code 2020: Day 20
"""

import os
import sys
import itertools
from pathlib import Path
from typing import Iterator
import operator
import functools
from collections import defaultdict


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


def flip_rows(rows: list[str]) -> list[str]:
    """
    Flip a list of strings on a top-left to bottom-right diagonal

    :param rows: list of strings
    :return: flipped list of strings
    """

    return list(reversed(rows.copy()))


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


def read_tiles(file: Path) -> Iterator[dict[str, any]]:
    """
    Read tiles from a given file

    :param file: file containing the input values
    :return: stream of maps
    """

    EXPECTED_TILE_LINES = 11

    def read_file_sections_(file_: Path) -> Iterator[list[str]]:
        """
        Nested function slicing file contents in sections

        :param file_: file containing the input values
        :return: stream of list of strings
        """

        lines_ = list()
        for line in open(file_):
            line_has_contents = len(line) > len(os.linesep)
            if line_has_contents:
                lines_.append(line.strip())
            else:
                yield lines_
                lines_ = list()
        if lines_:
            yield lines_

    for lines in read_file_sections_(file_=file):
        assert len(lines) == EXPECTED_TILE_LINES
        id_: int = int(lines[0][5:-1])
        rows: list[str] = lines[1:]
        yield {
            'id': id_,
            'rows': rows,
            'borders': get_borders(rows=rows),
        }


def get_borders(rows: list[str]) -> dict[str, str]:
    borders = dict()
    borders['N'] = rows[0]
    borders['E'] = ''.join([r[-1] for r in rows])
    borders['S'] = rows[-1]
    borders['W'] = ''.join([r[0] for r in rows])
    return borders


def compute_transforms(tile: dict[str, any]) -> dict[str, any]:
    """
    Compute possible tile transformations

    :param tile: tile data
    :return: enriched tile data
    """

    retval = dict(tile)
    transforms = list()
    for i in range(8):
        do_flip = i >= 4
        do_rotate = 90 * (i % 4)
        rows = transform_rows(rows=tile['rows'], flip=do_flip, rotate=do_rotate)
        transform = {
            'flip': do_flip,
            'rotate': do_rotate,
            'rows': rows,
            'borders': get_borders(rows=rows),
        }
        transforms.append(transform)
    retval['transforms'] = transforms
    return retval


def transform_rows(rows: list[str], rotate: int, flip: bool) -> list[str]:
    """
    Transform a given row of strings according to the given arguments

    :param rows: rows of string
    :param rotate: CW rotation angle in degres
    :param flip: flip the row of strings if True
    :return: transformed rows of string
    """

    rows_ = list(rows)
    assert rotate % 90 == 0
    rotations = rotate // 90
    for cw_rotations in range(rotations):
        rows_ = rotate_cw(rows_)
    rows_ = rows_ if not flip else flip_rows(rows=rows_)
    return rows_


def map_by_border(tiles: list[dict[str, any]]) -> dict[str, list]:

    border_map = defaultdict(list)
    for tile in tiles:
        id = tile['id']
        for t in tile['transforms']:
            for border in t['borders'].values():
                border_map[border].append({'id': id, 'transforms': t})
    return border_map


def map_by_tile(
        tiles: list[dict[str, any]],
        borders: dict[str, list]) -> dict[int, dict]:

    tile_map = defaultdict(dict)
    for tile in tiles:
        for t in tile['transforms']:
            border = t['rows'][0]
            id = tile['id']
            for b in [b for b in borders[border] if b['id'] != id]:
                if b['id'] in tile_map[id].values():
                    continue
                tile_map[id][b['id']] = b
    return tile_map


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


def assemble_tiles(tiles_by_id: dict[int, Tile], tile_map: list[list[tuple]]
                   ) -> list[list[str]]:
    """
    Assemble tiles

    :param tiles_by_id: tile instances by ID
    :param tile_map: array of tuple of tile ID and required transformation
    :return: list of strings
    """

    tile_size = len(list(tiles_by_id.values())[0]['rows'])
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
    matches = 0
    tries = 0

    for transform in range(8):
        monsters = find_monsters(image, pattern)
        if monsters:
            break
        #assert img != image
        # for i in range(image_size - pattern_vsize):
        #     v_crop = image[i:i + pattern_vsize]
        #     for j in range(image_size - pattern_hsize):
        #         crop = [r[j:j + pattern_hsize] for r in v_crop]
        #         c = correlate(a=crop, b=pattern)
        #         tries += 1
        #         if c:
        #             matches += 1
        #             print(crop)
        do_flip = transform == 4
        if not do_flip:
            image = rotate_cw(image)
        else:
            image = flip(image)

        print(tries)
    print(tries)


def read_(lines):
    tiles = "".join(lines).split("\n\n")
    for title, tile in (t.rstrip().split("\n", maxsplit=1) for t in tiles):
        tid = int(title.rstrip(":").split(maxsplit=1)[1])
        yield tid, list(parse(tile))


def parse(tile):
    tile = [list(r) for r in tile.replace("#", "1").replace(".", "0").splitlines()]
    for i in range(8):
        yield borders(tile), tile
        tile = list(rotate(tile))
        if i == 3:
            tile = [r[::-1] for r in tile]


def rotate(tile):
    for x in range(len(tile[0])):
        yield [r[-x - 1] for r in tile]


def borders(tile):
    left = int("".join(t[0] for t in tile), 2)
    right = int("".join(t[-1] for t in tile), 2)
    top = int("".join(tile[0]), 2)
    bot = int("".join(tile[-1]), 2)
    return left, right, top, bot


def find_monsters(image, pattern):
    monster_locs = []
    max_x, max_y = 0, 0
    for dy, line in enumerate(pattern):
        for dx, c in enumerate(line):
            if c == "#":
                monster_locs.append((dx, dy))
                max_x, max_y = max(dx, max_x), max((dy, max_y))

    monster_tiles = set()
    for y in range(len(image)):
        if y + max_y >= len(image):
            break
        for x in range(len(image[y])):
            if x + max_x >= len(image[y]):
                break
            has_monster = True
            for dx, dy in monster_locs:
                if image[y + dy][x + dx] != "#":
                    has_monster = False
                    break
            if has_monster:
                for dx, dy in monster_locs:
                    monster_tiles.add((x + dx, y + dy))
    if len(monster_tiles) == 0:
        return None

    all_squares = set()
    for y, line in enumerate(image):
        for x, c in enumerate(line):
            if c == "#":
                all_squares.add((x, y))
    return len(all_squares - monster_tiles)


def assemble(tiles):
    size = int(len(tiles) ** 0.5)
    return assemble_dfs(tiles, [[None] * size for _ in range(size)], set())


def assemble_dfs(tiles, img, placed, row=0, col=0):
    rc = row, col + 1
    if col == len(img) - 1:
        rc = row + 1, 0
    # for tile_data in tiles:
    #     tid = tile_data['id']
    #     tile = list(tile_data['borders'].values()), 42
    for tid, tile in tiles.items():
        if tid not in placed:
            placed.add(tid)
            for i, ((left, right, top, bot), ith_tile) in enumerate(tile):
                if (row > 0 and img[row - 1][col][1] != top) or (
                    col > 0 and img[row][col - 1][0] != left
                ):
                    continue
                img[row][col] = right, bot, tid, i, ith_tile
                assemble_dfs(tiles, img, placed, *rc)
                if len(placed) == len(tiles):
                    return img
            placed.remove(tid)


def concat(img):
    size = len(img) * (len(img[0][0][-1]) - 2)
    final_img = [[] for _ in range(size)]
    r = 0
    for row in img:
        for *_, tile in row:
            for y, line in enumerate(tile[1:-1]):
                final_img[r + y] += line[1:-1]
        r += len(tile) - 2
    return final_img


def find_sea_monsters(img, monster, monster_length):
    for i in range(8):
        count = 0
        img_dec = [int("".join(row), 2) for row in img]
        for r, rows in enumerate(zip(img_dec[:-2], img_dec[1:-1], img_dec[2:]), 1):
            for s in range(len(img[0]) - monster_length):
                count += all(r & m << s == m << s for r, m in zip(rows, monster))
        if count:
            return count
        img = list(rotate(img))
        if i == 3:
            img = [r[::-1] for r in img]


def process_part2(file: Path) -> int:
    """
    Compute the submission value from contents in the given file

    :param file: content file
    :return: value to submit
    """

    raw_tiles = list(read_tiles(file=file))
    tiles = [compute_transforms(tile=t) for t in raw_tiles]
    tiles_by_border = map_by_border(tiles=tiles)
    border_by_tiles = map_by_tile(tiles=tiles, borders=tiles_by_border)

    tiles_by_id = {t['id']: t for t in list(read_tiles(file=file))}
    tile_transforms = {id: compute_transformations(tile['rows']) for id, tile in tiles_by_id.items()}
    tile_map = arrange_tiles(tile_map=tile_transforms)

    tf2 = {tile['id']: [tt['rows'] for tt in tile['transforms']] for tile in tiles}
    tm2 = arrange_tiles(tile_map=tf2)

    #image = assemble_tiles(tiles_by_id=tiles_by_id, tile_map=tile_map)
    # image = remove_borders(image=image, size=10)

    tiles__ = dict(read_(l for l in open(file)))
    image__ = assemble(tiles__)
    concat__ = concat(image__)
    pattern = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ']
    monster = [int(seg.replace(" ", "0").replace("#", "1"), 2) for seg in pattern]
    monster_length = len(pattern[0])
    monster_weight = "".join(pattern).count("#")
    monsters = find_sea_monsters(concat__, monster, monster_length)
    submission = "".join("".join(r) for r in concat__).count("1") - monsters * monster_weight
    # image = search_pattern(image=image, pattern=pattern)
    #image = find_monsters(image=image, pattern=pattern)

    return submission


# Main -------------------------------------------------------------------------


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    files = ['./example.txt', './input.txt']
    files = ['./example.txt']
    files = ['./input.txt']
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


if __name__ == '__main__':
    sys.exit(main())
