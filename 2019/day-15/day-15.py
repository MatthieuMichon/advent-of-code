#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 15
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
from pathlib import Path

log = logging.getLogger(__name__)

EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


# High-level Data Structures ---------------------------------------------------

class Movement(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class StatusCodes(IntEnum):
    BLOCKED = 0
    MOVED_NO_OXYGEN = 1
    MOVED_GOT_OXYGEN = 2


STATUS = {
    StatusCodes.BLOCKED: {
        'update_position': False,
        'on_oxygen': False
    },
    StatusCodes.MOVED_NO_OXYGEN: {
        'update_position': True,
        'on_oxygen': False
    },
    StatusCodes.MOVED_GOT_OXYGEN: {
        'update_position': True,
        'on_oxygen': True
    },
}


# Common Methods ---------------------------------------------------------------

def load_contents(filename: Path) -> Iterator[map]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding a map of the address and its intcode
    """
    lines = iter(open(filename).read().strip().split(os.linesep))
    for line in lines:
        yield {i: int(token) for i, token in enumerate(line.split(','))}
    log.debug(f'Reached end of {filename=}')


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

    def __init__(self, message=''):
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

def compute_next_move(current_position, area_map, last_move) -> tuple:
    """Compute following movement depending on area map and last movement

    :param current_position:
    :param area_map:
    :param last_move:
    :return:
    """
    next_move = None
    positions = {
        'north': (current_position[0], current_position[1] + 1),
        'east': (current_position[0] + 1, current_position[1]),
        'south': (current_position[0], current_position[1] - 1),
        'west': (current_position[0] - 1, current_position[1]),
    }
    visited = {
        'north': positions['north'] in area_map,
        'east': positions['east'] in area_map,
        'south': positions['south'] in area_map,
        'west': positions['west'] in area_map,
    }
    if last_move == Movement.NORTH:
        if not visited['east']:
            next_move = Movement.EAST
        elif not visited['north']:
            next_move = Movement.NORTH
        else:
            raise Exception('stuck')
    elif last_move == Movement.EAST:
        if not visited['south']:
            next_move = Movement.SOUTH
        elif not visited['east']:
            next_move = Movement.EAST
        else:
            raise Exception('stuck')
    elif last_move == Movement.SOUTH:
        if not visited['west']:
            next_move = Movement.WEST
        elif not visited['south']:
            next_move = Movement.SOUTH
        else:
            raise Exception('stuck')
    elif last_move == Movement.WEST:
        if not visited['north']:
            next_move = Movement.NORTH
        elif not visited['west']:
            next_move = Movement.WEST
        else:
            raise Exception('stuck')
    return next_move


def solve_part_one(program: dict[int, int]) -> int:
    droid_position = (0, 0)
    area = {droid_position: 'D'}
    pc = 0
    rb = 0
    inputs = [Movement.NORTH]
    trail = [Movement.NORTH]
    outputs = []
    while len(outputs) == 0 or outputs[0] != StatusCodes.MOVED_GOT_OXYGEN:
        while len(inputs) > 0 or len(outputs) == 0:
            instruction = program[pc]
            opcode, operand_modes = decode(instruction=instruction)
            load_modes = operand_modes[:ISA[opcode].load_args]
            log.debug(f'{pc=} {instruction=} {ISA[opcode]} {operand_modes=} {load_modes=}')
            halt = ISA[opcode].name == 'Halt'
            input_required = ISA[opcode].name == 'In' and len(inputs) == 0
            operands = fetch(
                instruction_pointer=pc, load_modes=load_modes, ram=program,
                relative_base=rb, opcode=opcode, input_stack=inputs)
            output = execute(opcode=opcode, operands=operands)
            store_mode = operand_modes[-ISA[opcode].store_args:][0]
            store(opcode=opcode, store_mode=store_mode, output=output,
                  instruction_pointer=pc, ram=program, relative_base=rb)
            outputs = push_output(opcode=opcode, output=output)
            rb += shift_base(opcode=opcode, output=output)
            next_instruction_pointer = jump_next_instruction(
                opcode=opcode, instruction_pointer=pc, operands=operands)
            pc = next_instruction_pointer
        assert len(inputs) == 0
        last_move = trail[-1]
        if last_move == Movement.NORTH:
            target_position = (droid_position[0], droid_position[1] + 1)
        elif last_move == Movement.EAST:
            target_position = (droid_position[0] + 1, droid_position[1])
        elif last_move == Movement.SOUTH:
            target_position = (droid_position[0], droid_position[1] - 1)
        else:
            target_position = (droid_position[0] - 1, droid_position[1])
        state = StatusCodes(outputs[0])
        moved = state != StatusCodes.BLOCKED
        if moved:
            droid_position = target_position
            found_oxygen = state == StatusCodes.MOVED_GOT_OXYGEN
            if found_oxygen:
                area[target_position] = 'O'
            else:
                area[target_position] = '.'
        else:
            area[target_position] = '#'
        next_move = compute_next_move(current_position=droid_position, area_map=area, last_move=last_move)
        inputs = [next_move]
        trail.append(next_move)
        print('stop')
    answer = 0
    return answer


# Support Methods --------------------------------------------------------------

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
        answer = solve_part_one(program=contents)
        print(f'part one: {answer=}')
    if compute_part_two:
        contents = next(load_contents(filename=args.filename))
        answer = 0
        print(f'part two: {answer=}')
        return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
