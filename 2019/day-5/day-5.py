#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 5
Puzzle Solution in Python
"""

import argparse
import logging
import operator
import sys
from functools import reduce

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


INSTR_MAP = {
    1: {'length': 4},
    2: {'length': 4},
    3: {'length': 2},
    4: {'length': 2},
    5: {'length': 3},
    6: {'length': 3},
    7: {'length': 4},
    8: {'length': 4},
    99: {'length': 0},
}


def load_contents(filename: str) -> list[int]:
    """Load and convert contents from file

    :param filename: input filename
    :return: list of integer values
    """
    contents = list(map(int, open(filename).read().strip().split(',')))
    log.info(f'Loaded {len(contents)} values from {filename}')
    return contents


def decode_modes(instruction: int) -> list[int]:
    """Decode argument modes

    :param instruction: instruction
    :return: list of argument modes
    """
    opcode = int(str(instruction)[-2:])
    instr_args_qty = INSTR_MAP[opcode]['length'] - 1
    modes_str = list(str(instruction)[:-2])
    modes = list(reversed([int(m) for m in modes_str]))
    modes = list(modes) + [0] * (instr_args_qty - len(modes))
    log.debug(f'instr {instruction} -> modes {modes}')
    return modes


def execute(instr_ptr: int, contents: list[int], last_output: int) -> (int, int):
    """Execute the selected instruction

    :param instr_ptr: index
    :param contents: list of integers
    :param last_output: previous output value from last instruction
    :return: next instruction pointer, output integer
    """
    instr = contents[instr_ptr]
    opcode = int(str(instr)[-2:])
    param_modes = decode_modes(instruction=instr)
    assert opcode in INSTR_MAP
    output = last_output
    arguments = list()
    for i, mode in enumerate(param_modes):
        argument = contents[instr_ptr + i + 1]
        position_mode = 0 == mode
        if position_mode:
            log.debug(f'arg #{i}, ptr: {argument} val: {contents[argument]}')
            arguments.append(contents[argument])
        else:
            log.debug(f'arg #{i}, val: {argument}')
            arguments.append(argument)
    if opcode == 1:
        result = sum(arguments[:-1])
        result_ptr = contents[instr_ptr + len(param_modes)]
        contents[result_ptr] = result
        next_instr = instr_ptr + INSTR_MAP[opcode]['length']
    elif opcode == 2:
        result = reduce(operator.mul, arguments[:-1], 1)
        result_ptr = contents[instr_ptr + len(param_modes)]
        contents[result_ptr] = result
        next_instr = instr_ptr + INSTR_MAP[opcode]['length']
    elif opcode == 3:
        next_instr = instr_ptr + INSTR_MAP[opcode]['length']
        raise Exception
    elif opcode == 4:
        output = arguments[0]
        next_instr = instr_ptr + INSTR_MAP[opcode]['length']
        log.info(f'output: {output}')
    elif opcode == 5:
        non_zero = 0 != arguments[0]
        if non_zero:
            next_instr = arguments[1]
        else:
            next_instr = instr_ptr + INSTR_MAP[opcode]['length']
    elif opcode == 6:
        zero = 0 == arguments[0]
        if zero:
            next_instr = arguments[1]
        else:
            next_instr = instr_ptr + INSTR_MAP[opcode]['length']
    elif opcode == 7:
        less_than = arguments[0] < arguments[1]
        result_ptr = contents[instr_ptr + len(param_modes)]
        log.debug(f'contents: {contents}; result_pt {result_ptr}')
        if less_than:
            contents[result_ptr] = 1
        else:
            contents[result_ptr] = 0
        next_instr = instr_ptr + INSTR_MAP[opcode]['length']
    elif opcode == 8:
        equals = arguments[0] == arguments[1]
        result_ptr = contents[instr_ptr + len(param_modes)]
        if equals:
            contents[result_ptr] = 1
        else:
            contents[result_ptr] = 0
        next_instr = instr_ptr + INSTR_MAP[opcode]['length']
    elif opcode == 99:
        next_instr = instr_ptr + INSTR_MAP[opcode]['length']
        return -1, last_output
    return next_instr, output


# Puzzle Solving Methods -------------------------------------------------------


def execute_program(contents: list[int], input_: int) -> int:
    """Solve part one of the puzzle

    :param contents: list of integers
    :param input_: list of integers
    :return: output value
    """
    instr_ptr = 0
    assert contents[instr_ptr] == 3
    contents[contents[1]] = input_
    instr_ptr = 2
    output = -1
    while instr_ptr != -1:
        (instr_ptr, output) = execute(
            instr_ptr=instr_ptr, contents=contents, last_output=output)
    log.debug(f'contents: {contents}')
    return output


def solve(contents: list[int]) -> int:
    """Solve part one of the puzzle

    :param contents: list of integers
    :return: answer for the part one of the puzzle
    """
    output = execute_program(contents=contents, input_=1)
    return output


def solve_part_two(contents: list[int]) -> int:
    """Solve part two of the puzzle

    :param contents: list of integers
    :return: answer for the part one of the puzzle
    """
    output = execute_program(contents=contents, input_=5)
    return output


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = ('%(asctime)s - %(levelname)s - %(message)s')


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
        answer = solve(contents=contents)
        print(answer)
    if compute_part_two:
        contents = load_contents(filename=args.filename)
        answer = solve_part_two(contents=contents)
        print(answer)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
