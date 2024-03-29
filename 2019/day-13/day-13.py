#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 13
Puzzle Solution in Python
"""

import argparse
import logging
import os
import sys

from collections import Counter
from enum import IntEnum
from types import SimpleNamespace as sn
from typing import Iterator

log = logging.getLogger(__name__)


class TilesTypes(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZONTAL_PADDLE = 3
    BALL = 4


class Joystick(IntEnum):
    NEUTRAL = 0
    LEFT = -1
    RIGHT = 1


# Common Methods ---------------------------------------------------------------


def load_contents(filename: str) -> Iterator[map]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding a list of integers
    """
    lines = open(filename).read().strip().split(os.linesep)
    for line in lines:
        yield {i: int(token) for i, token in enumerate(line.split(','))}


# Intcode Methods --------------------------------------------------------------


INTCODE_INSTR_MOD = 100
DEFAULT_RAM_VALUE = 0
ISA = {
    1: sn(name='Add', input_args=0, load_args=2, store_args=1, output_args=0, jump=False),
    2: sn(name='Mul', input_args=0, load_args=2, store_args=1, output_args=0, jump=False),
    3: sn(name='In', input_args=1, load_args=0, store_args=1, output_args=0, jump=False),
    4: sn(name='Out', input_args=0, load_args=1, store_args=0, output_args=1, jump=False),
    5: sn(name='JNZ', input_args=0, load_args=2, store_args=0, output_args=0, jump=True),
    6: sn(name='JZ', input_args=0, load_args=2, store_args=0, output_args=0, jump=True),
    7: sn(name='LT', input_args=0, load_args=2, store_args=1, output_args=0, jump=False),
    8: sn(name='Eq', input_args=0, load_args=2, store_args=1, output_args=0, jump=False),
    9: sn(name='RBS', input_args=0, load_args=1, store_args=0, output_args=0, jump=False),
    99: sn(name='Halt', input_args=0, load_args=0, store_args=0, output_args=0, jump=False),
}


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class Mode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class OpcodeError(Error):
    """Exception raised for unsupported opcode.

    Attributes:
        opcode -- opcode value
    """

    def __init__(self, opcode: int):
        message = f'Invalid opcode {opcode}'
        super().__init__(message)


class HaltOpcode(Error):
    """Exception when an HALT opcode is encountered.

    Attributes:
        opcode -- opcode value
    """

    def __init__(self, message=""):
        super().__init__(message)


def decode(instruction: int) -> [int, list[int]]:
    """Decode instruction into opcode and load modes

    :param instruction: instruction
    :return: opcode and access mode per loaded arguments
    """
    opcode = instruction % INTCODE_INSTR_MOD
    if opcode not in ISA:
        raise OpcodeError(opcode=opcode)
    args_qty = ISA[opcode].load_args + ISA[opcode].store_args
    modes_int = instruction // INTCODE_INSTR_MOD
    modes = [Mode(int(m)) for m in reversed(str(modes_int))]
    leading_zero_modes = [Mode.POSITION] * (args_qty - len(modes))
    padded_modes = modes + leading_zero_modes
    log.debug(f'{instruction=}: {ISA[opcode].name}, {padded_modes}')
    return opcode, padded_modes


def fetch(instruction_pointer: int, load_modes: list[int], ram: dict[int, int],
          relative_base: int, opcode: int, input_stack: list[int]) -> list[int]:
    """Fetch operands from memory

    :param instruction_pointer: instruction operation code
    :param load_modes: access mode per loaded arguments
    :param ram: memory contents mapping
    :param relative_base: relative base address value
    :param opcode: instruction opcode
    :param input_stack: initial input value list
    :return: operand values
    """
    operands = list()
    if ISA[opcode].input_args > 0:
        for _ in range(ISA[opcode].input_args):
            value = input_stack.pop()
            operands.append(value)
    else:
        for i, mode in enumerate(load_modes):
            pointer = instruction_pointer + 1 + i
            contents = ram[pointer]
            if mode == Mode.IMMEDIATE:
                log.debug(f'argument {i}: mode {str(mode)}, value {contents}')
                operands.append(contents)
            elif mode == Mode.POSITION:
                log.debug(f'argument {i}: mode {str(mode)}, position {contents}, value {ram[contents]}')
                #operands.append(ram.get(contents, DEFAULT_RAM_VALUE))
                operands.append(ram[contents])
            elif mode == Mode.RELATIVE:
                log.debug(f'argument {i}: mode {str(mode)}, position {relative_base + contents}, value {ram[relative_base + contents]}')
                operands.append(ram[relative_base + contents])
            else:
                raise Exception
    log.debug(f'{operands=}')
    return operands


def execute(opcode: int, operands: list[int]) -> int:
    """Execute an instruction

    :param opcode: instruction opcode
    :param operands: operand values
    :return:
    """
    result = None
    if ISA[opcode].name == 'Add':
        result = sum(operands)
    if ISA[opcode].name == 'Mul':
        result = operands[0] * operands[1]
    if ISA[opcode].name == 'In':
        result = operands[0]
    if ISA[opcode].name == 'Out':
        result = operands[0]
    if ISA[opcode].name == 'LT':
        result = 1 if operands[0] < operands[1] else 0
    if ISA[opcode].name == 'Eq':
        result = 1 if operands[0] == operands[1] else 0
    if ISA[opcode].name == 'JNZ':
        result = operands[1]
    if ISA[opcode].name == 'JZ':
        result = operands[1]
    if ISA[opcode].name == 'RBS':
        result = operands[0]
    assert result is not None
    log.debug(f'executed {opcode=}, {operands=}, {result=}')
    return result


def store(
        opcode: int,
        store_mode: int,
        output: int,
        instruction_pointer: int,
        ram: dict[int, int],
        relative_base: int) -> None:
    """Store output value back into memory

    :param opcode: instruction opcode
    :param store_mode: stored operand mode
    :param output: output after execution of the instruction
    :param instruction_pointer: pointer to the current instruction
    :param ram: memory contents mapping
    :param relative_base: relative base address value
    :return: nothing
    """
    no_store = ISA[opcode].store_args == 0
    if no_store:
        return
    if store_mode == Mode.RELATIVE:
        store_pointer_address = instruction_pointer + 1 + ISA[opcode].load_args
        #store_pointer = relative_base + ram.get(store_pointer_address, DEFAULT_RAM_VALUE)
        store_pointer = relative_base + ram[store_pointer_address]
    elif store_mode == Mode.POSITION:
        store_pointer_address = instruction_pointer + 1 + ISA[opcode].load_args
        store_pointer = ram[store_pointer_address]
    else:
        raise Exception
    ram[store_pointer] = output
    log.debug(f'stored {output} @{store_pointer}')
    return


def push_output(opcode: int, output: int) -> list[int]:
    """Push value in the output stack

    :param opcode: instruction opcode
    :param output: output after execution of the instruction
    :return: new value to push to the output stack
    """
    output_ = list()
    if ISA[opcode].name == 'Out':
        output_.append(output)
    return output_


def shift_base(opcode: int, output: int) -> int:
    """Compute relative base shift

    :param opcode: instruction opcode
    :param output: output after execution of the instruction
    :return: relative base shift value
    """
    shift = 0
    if ISA[opcode].name == 'RBS':
        shift = output
    return shift


def jump_next_instruction(opcode: int, instruction_pointer: int,
                          operands: list[int]) -> int:
    """Compute pointer to following instruction

    :param opcode: instruction opcode
    :param instruction_pointer: pointer to the current instruction
    :param operands: operand values
    :return: pointer to following instruction
    """
    next_instruction = instruction_pointer + 1 + \
        ISA[opcode].load_args + ISA[opcode].store_args
    if ISA[opcode].name in ['Add', 'Mul', 'RBS', 'LT', 'Eq', 'In', 'Out']:
        pass
    elif ISA[opcode].name == 'JNZ':
        non_zero = operands[0] != 0
        next_instruction = operands[1] if non_zero else next_instruction
    elif ISA[opcode].name == 'JZ':
        non_zero = operands[0] == 0
        next_instruction = operands[1] if non_zero else next_instruction
    else:
        raise Exception
    log.debug(f'{opcode=}, {next_instruction=}')
    return next_instruction


# Solver Methods ---------------------------------------------------------------


def step(ram: dict, regs: dict, inputs: list[int]) -> tuple:
    """Advance robot by a single step

    :param ram: memory contents
    :param regs: register map
    :param inputs: input queue
    :return: updated pc; new color and turn direction
    """
    pc = regs['pc']
    relative_base = regs['rb']
    output_values = list()
    while True:
        instruction = ram[pc]
        opcode, operand_modes = decode(instruction=instruction)
        halt = ISA[opcode].name == 'Halt'
        if halt:
            break
        load_modes = operand_modes[:ISA[opcode].load_args]
        operands = fetch(instruction_pointer=pc,
                         load_modes=load_modes, ram=ram,
                         relative_base=relative_base,
                         opcode=opcode, input_stack=inputs)
        output = execute(opcode=opcode, operands=operands)
        store_mode = operand_modes[-ISA[opcode].store_args:][0]
        store(opcode=opcode, store_mode=store_mode, output=output,
              instruction_pointer=pc, ram=ram,
              relative_base=relative_base)
        output_values.extend(push_output(opcode=opcode, output=output))
        relative_base += shift_base(opcode=opcode, output=output)
        next_instruction_pointer = jump_next_instruction(
            opcode=opcode, instruction_pointer=pc, operands=operands)
        pc = next_instruction_pointer
    regs['pc'] = pc
    regs['rb'] = relative_base
    return tuple(output_values)


def map_tiles(tiles: [int, int, int]) -> dict:
    """Map a list in of tiles

    :param tiles: list of tiles
    :return: dict representation
    """
    d = {(x, y): id_ for (x, y, id_) in tiles}
    return d


def solve(contents: map) -> int:
    """Solve puzzle part one

    :param contents: puzzle input contents
    :return: puzzle answer
    """
    regs = {'pc': 0, 'rb': 0}
    output_values = step(ram=contents, regs=regs, inputs=[])
    assert len(output_values) % 3 == 0
    tiles_count: int = len(output_values) // 3
    tiles = [output_values[3 * i:3 * i + 3] for i in range(tiles_count)]
    map_ = map_tiles(tiles=tiles)
    pic = []
    for y in range(min(map_.keys())[1], max(map_.keys())[1]+1):
        line = []
        for x in range(min(map_.keys())[0], max(map_.keys())[0]+1):
            if map_[(x, y)] == TilesTypes.BLOCK:
                line.append('x')
            elif map_[(x, y)] == TilesTypes.WALL:
                line.append('#')
            elif map_[(x, y)] == TilesTypes.EMPTY:
                line.append(' ')
            elif map_[(x, y)] == TilesTypes.HORIZONTAL_PADDLE:
                line.append('=')
            elif map_[(x, y)] == TilesTypes.BALL:
                line.append('o')
        print(''.join(line))
        pic.append(line)
    tile_ids = [tile[2] for tile in tiles]
    block_tiles = Counter(tile_ids)[TilesTypes.BLOCK]
    return block_tiles


def print_map(map_):
    for y in set(k[1] for k in map_.keys()):
        line = []
        for x in set(k[0] for k in map_.keys()):
            if x == -1:
                continue
            if (x, y) not in map_:
                continue
            if map_[(x, y)] == TilesTypes.BLOCK:
                line.append('x')
            elif map_[(x, y)] == TilesTypes.WALL:
                line.append('#')
            elif map_[(x, y)] == TilesTypes.EMPTY:
                line.append(' ')
            elif map_[(x, y)] == TilesTypes.HORIZONTAL_PADDLE:
                line.append('=')
            elif map_[(x, y)] == TilesTypes.BALL:
                line.append('o')
        print(''.join(line))


def step_part_two(
        ram: dict, regs: dict, inputs: list[int],
        tiles: list[list[int]]) -> int:
    """Advance robot by a single step

    :param ram: memory contents
    :param regs: register map
    :param inputs: input queue
    :param tiles: list of tiles
    :return: ball position on the horizontal axis
    """
    pc = regs['pc']
    relative_base = regs['rb']
    tile = []
    while True:
        instruction = ram[pc]
        opcode, operand_modes = decode(instruction=instruction)
        halt = ISA[opcode].name == 'Halt'
        if halt:
            break
        load_modes = operand_modes[:ISA[opcode].load_args]
        operands = fetch(instruction_pointer=pc,
                         load_modes=load_modes, ram=ram,
                         relative_base=relative_base,
                         opcode=opcode, input_stack=inputs)
        output = execute(opcode=opcode, operands=operands)
        store_mode = operand_modes[-ISA[opcode].store_args:][0]
        store(opcode=opcode, store_mode=store_mode, output=output,
              instruction_pointer=pc, ram=ram,
              relative_base=relative_base)
        tile.extend(push_output(opcode=opcode, output=output))
        relative_base += shift_base(opcode=opcode, output=output)
        next_instruction_pointer = jump_next_instruction(
            opcode=opcode, instruction_pointer=pc, operands=operands)
        pc = next_instruction_pointer
        if len(tile) == 3:
            tiles.append([*tile[0:2], tile[2]])
            if tile[0] != -1 and tile[2] == TilesTypes.BALL:
                break
            tile = []
    regs['pc'] = pc
    regs['rb'] = relative_base


def print_score(tiles: map):
    assert (-1, 0) in tiles
    print(f'Score: {tiles[(-1, 0)]}')


def get_position(tiles: list, tile_type: TilesTypes) -> any:
    """Get object position

    :param tiles: map of tiles per coordinates
    :param tile_type: target tile type
    :return: position
    """
    filtered_tiles = [t[0:2] for t in tiles if t[2] == tile_type]
    if not len(filtered_tiles):
        return None
    return filtered_tiles[-1][0]


def solve_part_two(contents: map) -> int:
    """Solve puzzle part one

    :param contents: puzzle input contents
    :return: puzzle answer
    """
    contents[0] = 2

    regs = {'pc': 0, 'rb': 0}
    inputs = []
    tiles = []
    last_ball_position = None
    while True:
        step_part_two(ram=contents, regs=regs, inputs=inputs, tiles=tiles)
        map_ = map_tiles(tiles=tiles)
        tile_ids = list(map_.values())
        block_tiles = Counter(tile_ids)[TilesTypes.BLOCK]
        if block_tiles == 0:
            print_map(map_)
            print('done')
            return map_[(-1, 0)]
        paddle_position = get_position(
            tiles=tiles, tile_type=TilesTypes.HORIZONTAL_PADDLE)
        if paddle_position is None:
            inputs.append(Joystick.NEUTRAL)
            continue
        ball_position = get_position(
            tiles=tiles, tile_type=TilesTypes.BALL)
        if last_ball_position is None:
            last_ball_position = ball_position
        next_ball_position = ball_position + (ball_position - last_ball_position)
        if next_ball_position < paddle_position:
            inputs.append(Joystick.LEFT)
        elif next_ball_position == paddle_position:
            inputs.append(Joystick.NEUTRAL)
        elif next_ball_position > paddle_position:
            inputs.append(Joystick.RIGHT)
        last_ball_position = ball_position


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
        contents = next(load_contents(filename=args.filename))
        answer = solve(contents=contents)
        print(f'part one: {answer=}')
    if compute_part_two:
        contents = next(load_contents(filename=args.filename))
        answer = solve_part_two(contents=contents)
        print(f'part two: {answer=}')
        return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
