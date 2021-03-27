#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 9
Puzzle Solution in Python
"""

import argparse
import logging
import os
import sys

from collections import ChainMap
from enum import IntEnum
from types import SimpleNamespace as sn
from typing import Iterator

log = logging.getLogger(__name__)

INTCODE_INSTR_MOD = 100
ISA = {
    2: sn(name='Add', input_args=0, load_args=2, store_args=1, output_args=0),
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
        self.opcode = opcode


# Common Methods ---------------------------------------------------------------


def load_contents(filename: str) -> Iterator[list[int]]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding a list of integers
    """
    lines = open(filename).read().strip().split(os.linesep)
    for line in lines:
        yield [int(token) for token in line.split(',')]


def decode(instruction: int) -> [int, list[int]]:
    """Decode instruction into opcode and load modes

    :param instruction: instruction
    :return: opcode and list modes per loaded arguments
    """
    opcode = instruction % INTCODE_INSTR_MOD
    if opcode not in ISA:
        raise OpcodeError(opcode)
    loaded_args = ISA[opcode].load_args
    modes_int = instruction // INTCODE_INSTR_MOD
    modes = [Mode(int(m)) for m in reversed(str(modes_int))]
    leading_zero_modes = [Mode.IMMEDIATE] * (loaded_args - len(modes))
    padded_modes = modes + leading_zero_modes
    return opcode, padded_modes


def execute_program(
        ram: dict[int, int],
        instruction_pointer: int,
        input_stack: list[int]) -> list[int]:
    """Execute an Intcode program stored in RAM

    :param ram: memory contents mapping
    :param instruction_pointer: initial instruction pointer value
    :param input_stack: initial input value list
    :return: output values
    """
    output_values = list()
    while True:
        instruction = ram[instruction_pointer]
        opcode, load_modes = decode(instruction=instruction)
        halt = opcode == ISA.halt.opcode
        if halt:
            break
    return  output_values


# Solver Methods ---------------------------------------------------------------


def solve(contents: [int]) -> int:
    """Solve puzzle part one

    :param contents: Intcode program
    :return: puzzle answer
    """
    mem = {k: v for k, v in enumerate(contents)}
    inputs = [1]
    outputs = execute_program(
        ram=mem, instruction_pointer=0, input_stack=inputs)
    return outputs[0]


def solve_part_two(contents) -> int:
    ...
    return -1


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-32s - %(levelname)-8s - %(message)s'


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
        for intcode in load_contents(filename=args.filename):
            answer = solve(contents=intcode)
            print(f'part one: answer: {answer}')
    if compute_part_two:
        for intcode in load_contents(filename=args.filename):
            answer = solve_part_two(contents=intcode)
            print(f'part two: answer: {answer}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
