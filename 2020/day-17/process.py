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


# Common -----------------------------------------------------------------------


def list_indexes(state: dict[tuple, any], axis: int) -> list:
    """
    Get the indexes of an axis on a state mapping

    :param state:
    :param axis:
    :return: set of indexes across the given axis
    """

    indexes = set(position[axis] for position in state.keys())
    index_list = sorted(indexes)
    return index_list


# Part One ---------------------------------------------------------------------


def visualize(state: dict[tuple[int, int, int], bool]) -> None:
    """

    :param state:
    :return:
    """

    for z in list_indexes(state, 2):
        print(f'z={z}')
        print(f'      {" ".join(str(c) for c in list_indexes(state, 0)):6}')
        print(f'      {" ".join("-" for c in list_indexes(state, 0)):6}')
        for y in list_indexes(state, 1):
            print(f'{y:3} - {" ".join("X" if state[(x, y, z)] else "." for x in list_indexes(state, 0))}')


def visualize_neighbors(neighbors: dict[tuple[int, int, int], int]) -> None:
    """
    Visualize a neighbors quantity map

    :param neighbors:
    :return: nothing
    """

    for z in list_indexes(neighbors, 2):
        print(f'z={z}')
        print(f'      {" ".join(str(c) for c in list_indexes(neighbors, 0)):6}')
        print(f'      {" ".join("-" for c in list_indexes(neighbors, 0)):6}')
        for y in list_indexes(neighbors, 1):
            print(f'{y:3} - {" ".join(str(neighbors[(x, y, z)]) for x in list_indexes(neighbors, 1))}')


def decode(file: Path) -> dict[tuple[int, int, int], bool]:
    """
    Decode file contents

    :param file:
    :return: 3d map of the initial slice
    """

    fh = open(file)
    decoded_map = dict()
    for i, l in enumerate(fh):
        for j, c in enumerate(l.strip()):
            active = True if c == '#' else False
            x = j
            y = i
            z = 0
            decoded_map[(x, y, z)] = active

    return decoded_map


def execute_cycle(state: dict[tuple[int, int, int], bool]) -> dict[tuple[int, int, int], bool]:
    """

    :param state: 3d mapping of the state
    :return: 3d mapping of the state
    """

    expanded_state = state
    for axis in range(3):
        state = copy.deepcopy(expanded_state)
        axis_values = list_indexes(state=state, axis=axis)
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
    #visualize(expanded_state)

    state_dd = defaultdict(bool, expanded_state)
    active_neighbors_map = dict()
    moves = [[-1, 0, +1]] * 3
    self = (0, 0, 0)
    directions = [m for m in list(itertools.product(*moves)) if m != self]
    for pos in expanded_state.keys():
        active_neighbors = 0
        for dir in directions:
            neighbor = tuple(pos[axis] + dir[axis] for axis in range(3))
            if state_dd[neighbor]:
                active_neighbors += 1
        active_neighbors_map[pos] = active_neighbors
    #visualize_neighbors(active_neighbors_map)

    updated_state = copy.copy(expanded_state)
    ACTIVE = True
    INACTIVE = False
    for pos, count in active_neighbors_map.items():
        cube_active = expanded_state[pos] == ACTIVE
        neighbors_active = active_neighbors_map[pos]
        if cube_active and neighbors_active not in [2, 3]:
            updated_state[pos] = INACTIVE
        elif not cube_active and neighbors_active == 3:
            updated_state[pos] = ACTIVE

    #visualize(updated_state)

    return updated_state


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    initial_slice = decode(file=file)
    visualize(state=initial_slice)

    state = initial_slice
    for cycle in range(6):
        visualize(state)
        new_state = execute_cycle(state=state)
        state = new_state

    active_cubes = sum(state.values())
    submission = active_cubes
    return submission


# Part Two


# Main


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    files = ['./example.txt', './input.txt']
    for f in files:
        print(f'In file {f}:')
        print(f'\tPart One: {process(file=Path(f))}')

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
