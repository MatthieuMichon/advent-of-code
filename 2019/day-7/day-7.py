#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 7
Puzzle Solution in Python
"""

import argparse
import itertools
import logging
import operator
import os
import sys
from enum import IntEnum
from functools import reduce

log = logging.getLogger(__name__)


# Intcode Common Methods -------------------------------------------------------


def load_contents(filename: str) -> list[list[int]]:
    """Load and convert contents from file

    :param filename: input filename
    :return: list of integer lists with variable length
    """
    lines = open(filename).read().strip().split(os.linesep)
    contents = [list(map(int, l.split(','))) for l in lines]
    log.info(f'Loaded {len(contents)} lists from {filename}, '
             f'with a total of {sum(len(l) for l in contents)} instructions')
    return contents


class Intcode(IntEnum):
    ADD = 1
    MUL = 2
    RD = 3
    WR = 4
    JNZ = 5
    JZ = 6
    ALT = 7
    AE = 8
    HALT = 99


class ParameterMode(IntEnum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1


opcode_map = {
    Intcode.ADD: {'parameters': 2},
    Intcode.MUL: {'parameters': 2},
    Intcode.RD: {'parameters': 0},
    Intcode.WR: {'parameters': 1},
    Intcode.JNZ: {'parameters': 2},
    Intcode.JZ: {'parameters': 2},
    Intcode.ALT: {'parameters': 2},
    Intcode.AE: {'parameters': 2},
    Intcode.HALT: {'parameters': 0},
}
MAX_PARAMETERS = max(opcode['parameters'] for opcode in opcode_map.values())


def decode_instruction(instruction: int) -> [int, list[int]]:
    """Decode instruction into opcode and parameter modes

    :param instruction: instruction
    :return: opcode and list of parameter modes
    """
    digits = list(map(int, str(instruction)))
    opcode = int(''.join(map(str, digits[-2:])))
    parameters = opcode_map[opcode]['parameters']
    modes = list(reversed(digits[:-2])) + [0] * (parameters - max(0, len(digits) - 2))
    log.debug(f'[{instruction}]: opcode {opcode}, parameters {modes}')
    return opcode, modes


def fetch_arguments(data: list[int], opcode_ptr: int,
                    parameter_modes: list[int]) -> list[int]:
    """Fetch arguments from Intcode data

    :param data: list of Intcode instructions
    :param opcode_ptr: opcode to be executed
    :param parameter_modes: opcode arguments parameter modes
    :return: opcode argument values
    """
    arguments = list()
    log.debug(f'@{opcode_ptr}->[{data[opcode_ptr]}], modes: {parameter_modes}')
    for i, parameter_mode in enumerate(parameter_modes):
        argument_address = opcode_ptr + 1 + i
        assert parameter_mode in ParameterMode.__members__.values()
        if parameter_mode == ParameterMode.POSITION_MODE:
            argument_ptr = data[argument_address]
            argument = data[argument_ptr]
        elif parameter_mode == ParameterMode.IMMEDIATE_MODE:
            argument = data[argument_address]
        else:
            raise Exception
        log.debug(f' - arg #{i}: mode {parameter_mode} addr {argument_address} val {argument}')
        arguments.append(argument)
    log.debug(f'@{opcode_ptr}->[{data[opcode_ptr]}], args: {arguments}')
    return arguments


def execute_opcode(data: list[int], opcode_ptr: int,
                   inputs: list[int]) -> [int, list[int], any]:
    """Execute the pointed instruction

    :param data: list of Intcode instructions
    :param opcode_ptr: opcode to be executed
    :param inputs: input value stack
    :return: next opcode pointer, updated input stack, output value or nothing
    """
    instruction = data[opcode_ptr]
    log.debug(f'Executing @{opcode_ptr}->[{instruction}]')
    opcode, parameter_modes = decode_instruction(instruction)
    assert Intcode(opcode) in opcode_map
    opcode_args = fetch_arguments(data=data, opcode_ptr=opcode_ptr,
                                  parameter_modes=parameter_modes)
    output = None
    if opcode == Intcode.ADD:
        output_ptr = data[opcode_ptr + opcode_map[opcode]['parameters'] + 1]
        output_value = sum(opcode_args)
        data[output_ptr] = output_value
        opcode_ptr += opcode_map[opcode]['parameters'] + 2
    elif opcode == Intcode.MUL:
        output_ptr = data[opcode_ptr + opcode_map[opcode]['parameters'] + 1]
        output_value = reduce(operator.mul, opcode_args, 1)
        data[output_ptr] = output_value
        opcode_ptr += opcode_map[opcode]['parameters'] + 2
    elif opcode == Intcode.RD:
        output_ptr = data[opcode_ptr + opcode_map[opcode]['parameters'] + 1]
        output_value = inputs.pop(0)
        data[output_ptr] = output_value
        opcode_ptr += opcode_map[opcode]['parameters'] + 2
    elif opcode == Intcode.WR:
        output = opcode_args[0]
        opcode_ptr += opcode_map[opcode]['parameters'] + 1
    elif opcode == Intcode.JNZ:
        jump = 0 != opcode_args[0]
        if jump:
            opcode_ptr = opcode_args[1]
        else:
            opcode_ptr += opcode_map[opcode]['parameters'] + 1
    elif opcode == Intcode.JZ:
        jump = 0 == opcode_args[0]
        if jump:
            opcode_ptr = opcode_args[1]
        else:
            opcode_ptr += opcode_map[opcode]['parameters'] + 1
    elif opcode == Intcode.ALT:
        output_ptr = data[opcode_ptr + opcode_map[opcode]['parameters'] + 1]
        less_than = opcode_args[0] < opcode_args[1]
        if less_than:
            output_value = 1
        else:
            output_value = 0
        data[output_ptr] = output_value
        opcode_ptr += opcode_map[opcode]['parameters'] + 2
    elif opcode == Intcode.AE:
        output_ptr = data[opcode_ptr + opcode_map[opcode]['parameters'] + 1]
        equals = opcode_args[0] == opcode_args[1]
        if equals:
            output_value = 1
        else:
            output_value = 0
        data[output_ptr] = output_value
        opcode_ptr += opcode_map[opcode]['parameters'] + 2
    elif opcode == Intcode.HALT:
        raise Exception
    return opcode_ptr, inputs, output


# Puzzle Solving Methods -------------------------------------------------------


AMPLIFIERS: int = 5
PHASE_RANGE: tuple = (0, 5)


def compute_output_signal(data: list[int], input_: int, phase: int) -> int:
    """Compute output signal value for an amplifier stage

    :param data: list of Intcode instructions
    :param input_: amplifier stage input value
    :param phase: amplifier stage phase setting
    :return: output value
    """
    inputs = [phase, input_]
    opcode_ptr: int = 0
    output: int = 0
    while data[opcode_ptr] != Intcode.HALT:
        opcode_ptr, inputs, output = execute_opcode(
            data=data, opcode_ptr=opcode_ptr, inputs=inputs)
    return output


def solve(contents: list[int]) -> int:
    """Solve part one of the puzzle

    :param contents: list of integers
    :return: answer for the part one of the puzzle
    """
    amp_outputs = list()
    phase_settings = itertools.permutations(
        iterable=range(*PHASE_RANGE), r=AMPLIFIERS)
    for phase_setting in phase_settings:
        amp_input = 0
        amp_output = 0
        for amp in range(AMPLIFIERS):
            amp_phase_setting = phase_setting[amp]
            temp_contents = contents.copy()
            amp_output = compute_output_signal(
                data=temp_contents, input_=amp_input,
                phase=amp_phase_setting)
            amp_input = amp_output
        amp_outputs.append(amp_output)
    answer = max(amp_outputs)
    return answer


def solve_part_two(contents: list[int]) -> int:
    """Solve part two of the puzzle

    :param contents: list of integers
    :return: answer for the part one of the puzzle
    """
    ...
    answer = -1
    return answer


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'


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
        for i, c in enumerate(contents):
            answer = solve(contents=c)
            print(f'index {i}, answer: {answer}')
    if compute_part_two:
        contents = load_contents(filename=args.filename)
        for i, c in enumerate(contents):
            answer = solve_part_two(contents=c)
            print(f'index {i}, answer: {answer}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
