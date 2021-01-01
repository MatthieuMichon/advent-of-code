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
from typing import List, Mapping, Union, Iterator
from pathlib import Path


DEBUG = False

TOKEN_DELIMITER: str = ' '
OPERATORS = ['+', '*']

# Common -----------------------------------------------------------------------


def decode(file: Path) -> Iterator[list[str]]:
    """
    Decode contents of the given file

    :param file: file containing the input values
    :return: list of tokens
    """

    for line in open(file):
        tokens = tokenize(expression=line)
        yield tokens


def tokenize(expression: str) -> list[str]:
    """
    Tokenize the given expression

    :param expression: line of text
    :return: list of tokens
    """

    expanded_expression: str = expression.replace('(', '( ').replace(')', ' )')
    tokens: list[str] = expanded_expression.strip().split(TOKEN_DELIMITER)

    return tokens


# Part One ---------------------------------------------------------------------


def convert_rpn(tokens: list[str]) -> list[Union[int, str]]:
    """
    Convert a list of token into a RPN sequence

    :param tokens: list of tokens
    :return: list of tokens in RPN sequence
    """

    output_queue = list()
    operator_stack = list()

    for t in tokens:
        if t.isnumeric():
            output_queue.append(int(t))
        elif t in ['+', '*']:
            while len(operator_stack) and operator_stack[-1] != '(':
                op = operator_stack.pop()
                output_queue.append(op)
            operator_stack.append(t)
        elif t == '(':
            operator_stack.append(t)
        elif t == ')':
            while operator_stack[-1] != '(':
                op = operator_stack.pop()
                output_queue.append(op)
            if operator_stack[-1] == '(':
                operator_stack.pop()
    while len(operator_stack):
        op = operator_stack.pop()
        output_queue.append(op)

    return output_queue


def evaluate(tokens: list[Union[int, str]]) -> int:
    """
    Evaluate a list of tokens ordered in RPN fashion

    :param tokens: list of tokens in RPN sequence
    :return: result of the arithmetic expression
    """

    stack: list[int] = list()
    for t in tokens:
        if t in OPERATORS:
            result: int = 0
            arg_a = stack.pop()
            arg_b = stack.pop()
            if t == '+':
                result = arg_a + arg_b
            if t == '*':
                result = arg_a * arg_b
            stack.append(result)
        else:
            stack.append(t)
    assert len(stack) == 1

    return stack.pop()


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    result: int = 0
    for tokens in decode(file=file):
        tokens = convert_rpn(tokens=tokens)
        result += evaluate(tokens=tokens)

    return result


# Part Two ---------------------------------------------------------------------


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
