#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day Two
Puzzle Solution in Python
"""

import argparse
import logging
import sys


EXIT_SUCCESS = 0
LOG_FORMAT = ('%(asctime)s - %(levelname)s - %(module)s - '
              '%(funcName)s - %(message)s')

log = logging.getLogger(__name__)


def load_contents(filename: str) -> list[int]:
    """Load contents from the given file

    :param filename: filename as string
    :return: list of integers
    """
    contents = list(map(int, open(filename).read().strip().split(',')))
    log.info(f'Loaded {len(contents)} values from {filename}')
    return contents


# Puzzle Solving Methods -------------------------------------------------------

ADD = 1
MUL = 2
HALT = 99


def patch(program: list[int]) -> list[int]:
    """Restore the gravity assist program

    :param program: Intcode program
    :return: patched Intcode program
    """
    program[1] = 12
    program[2] = 2
    return program


def solve(contents: list[int]):
    """Solve part one of the puzzle

    :param contents: list of integers
    :return: answer for the part one of the puzzle
    """

    def execute(instruction: int, operand_a: int, operand_b: int) -> int:
        """Evaluate operands using the given arithmetic instruction

        :param instruction: Intcode arithmetic instruction
        :param operand_a: first operand
        :param operand_b: second operand
        :return: result of the arithmetical instruction
        """
        if instruction == ADD:
            return operand_a + operand_b
        if instruction == MUL:
            return operand_a * operand_b

    input_program = len(contents) > 12
    program = patch(program=contents) if input_program else contents
    pc = 0
    instr = program[pc]
    while instr in [ADD, MUL]:
        a_ptr, b_ptr, r_ptr = program[pc + 1:pc + 4]
        a, b = [program[ptr] for ptr in [a_ptr, b_ptr]]
        program[r_ptr] = execute(instruction=instr, operand_a=program[a_ptr],
                                 operand_b=program[b_ptr])
        log.debug(f'pc: {pc:02x}, instr: {instr:02d}, a_ptr:{a_ptr}, a:{a}, '
                  f'b_ptr: {b_ptr}, b: {b}')
        pc += 4
        instr = program[pc]
    answer = program[0]
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
    contents = load_contents(filename=args.filename)
    compute_part_one = not args.part or 1 == args.part
    compute_part_two = not args.part or 2 == args.part
    compute_part_two = False
    if compute_part_one:
        answer = solve(contents=contents)
        print(answer)
    if compute_part_two:
        #answer = solve_part_two(contents=contents)
        print(answer)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
