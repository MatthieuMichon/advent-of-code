#!/usr/bin/env python
"""
Advent of Code 2020: Day 16
"""

import copy
from collections import defaultdict
import math
import itertools
import signal
import sys
from types import FrameType
from typing import List, Mapping
from pathlib import Path


DEBUG = False

ACTIVE = True
INACTIVE = False


# Common -----------------------------------------------------------------------


def decode(file: Path) -> dict[tuple[int, int], bool]:
    """
    Decode file contents

    :param file: file containing the input values
    :return: 2d map of the initial slice
    """

    fh = open(file)
    decoded_map = dict()
    for y, l in enumerate(fh):
        for x, c in enumerate(l.strip()):
            active = c == '#'
            decoded_map[(x, y)] = active

    return decoded_map


def list_indexes(map_: dict[tuple, any], axis: int) -> list:
    """
    List the indexes of a given axis in a mapping

    :param map_: mapping of a property (activation) per grid position
    :param axis: selected grid axis
    :return: set of indexes across the given axis
    """

    axis_count: int = len(next(iter(map_.keys())))
    if axis >= axis_count:
        return [0]
    indexes = set(position[axis] for position in map_.keys())
    index_list = sorted(indexes)
    return index_list


def visualize(map_: dict[tuple, any]) -> None:
    """
    Visualize slices of a mapping

    :param map_: mapping of a property (activation) per grid position
    :return: nothing
    """

    conv = lambda pos, axis_cnt: \
        ('X' if map_[pos[:axis_cnt]] else ".") if isinstance(
            map_[pos[:axis_cnt]], bool) else str(map_[pos[:axis_cnt]])

    axis_count: int = len(next(iter(map_.keys())))
    for w in list_indexes(map_, 3):
        for z in list_indexes(map_, 2):
            if axis_count == 4:
                print(f'z={z}, w={w}')
            elif axis_count == 3:
                print(f'z={z}')
            for y in list_indexes(map_, 1):
                print(f'{" ".join(conv((x, y, z, w), axis_count) for x in list_indexes(map_, 0))}')


def execute_cycle(state: dict[tuple, bool]) -> dict[tuple[int, int, int], bool]:
    """
    Execute one single state update cycle

    :param state: 3d mapping of the state
    :return: 3d mapping of the state
    """

    expanded_state = state
    axis_count: int = len(next(iter(state.keys())))
    for axis in range(axis_count):
        state = copy.copy(expanded_state)
        axis_values = list_indexes(map_=state, axis=axis)
        for upper in [True, False]:
            index = max(axis_values) if upper else min(axis_values)
            state_slice = {pos: v for pos, v in state.items()
                           if pos[axis] == index}
            slice_active = any(state_slice.values())
            if slice_active:
                new_index = index + (1 if upper else -1)
                for pos, s in state_slice.items():
                    new_pos = tuple(new_index if i == axis else a
                                    for i, a in enumerate(pos))
                    expanded_state[new_pos] = False
    if DEBUG:
        visualize(expanded_state)

    state_dd = defaultdict(bool, expanded_state)
    active_neighbors_map = dict()
    moves = [[-1, 0, +1]] * axis_count
    self = tuple([0] * axis_count)
    directions = [m for m in list(itertools.product(*moves)) if m != self]
    for pos in expanded_state.keys():
        active_neighbors = 0
        for dir_ in directions:
            neighbor = tuple(pos[axis] + dir_[axis] for axis in range(axis_count))
            if state_dd[neighbor]:
                active_neighbors += 1
        active_neighbors_map[pos] = active_neighbors
    if DEBUG:
        visualize(active_neighbors_map)

    updated_state = expanded_state #copy.copy(expanded_state)
    for pos, count in active_neighbors_map.items():
        cube_active = expanded_state[pos] == ACTIVE
        neighbors_active = active_neighbors_map[pos]
        if cube_active and neighbors_active not in [2, 3]:
            updated_state[pos] = INACTIVE
        elif not cube_active and neighbors_active == 3:
            updated_state[pos] = ACTIVE
    if DEBUG:
        visualize(updated_state)

    return updated_state


# Part One ---------------------------------------------------------------------


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    initial_slice = decode(file=file)
    initial_state = {pos + tuple([0]): state for pos, state in initial_slice.items()}
    if DEBUG:
        visualize(map_=initial_state)

    state = initial_state
    for cycle in range(6):
        if DEBUG:
            visualize(state)
        new_state = execute_cycle(state=state)
        state = new_state

    active_cubes = sum(state.values())
    submission = active_cubes
    return submission


# Part Two ---------------------------------------------------------------------


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    initial_slice = decode(file=file)
    initial_state = {pos + tuple([0, 0]): state
                     for pos, state in initial_slice.items()}
    if DEBUG:
        visualize(map_=initial_state)

    state = initial_state
    for cycle in range(6):
        if DEBUG:
            visualize(state)
        new_state = execute_cycle(state=state)
        state = new_state

    active_cubes = sum(state.values())
    submission = active_cubes
    return submission


# Main -------------------------------------------------------------------------


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    files = ['./example.txt', './input.txt']
    #files = ['./example.txt']
    #files = []
    for f in files:
        print(f'In file {f}:')
        print(f'\tPart One: {process(file=Path(f))}')

    files = ['./example.txt', './input.txt']
    #files = ['./example.txt']
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
