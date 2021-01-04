#!/usr/bin/env python
"""
Advent of Code 2020: Day 19
"""

import signal
import sys
from types import FrameType
import itertools
from pathlib import Path


DEBUG = False

SEPARATOR: str = ' '
RULE_NUMBER_SUFFIX = ':'

# Common -----------------------------------------------------------------------


def decode(file: Path) -> tuple[dict, list[str]]:
    """
    Decode contents of the given file

    :param file: file containing the input values
    :return: tuple of rule map and message list
    """

    fp = itertools.dropwhile(lambda l: l == '\n', open(file))
    convert = lambda t: int(t) if t.isnumeric() else t.replace('"', '')
    rule_map: dict[int, any] = dict()
    received_messages = list()
    for parts in (line.strip().split(RULE_NUMBER_SUFFIX) for line in fp):
        if len(parts) == 2:
            tokens = parts[1].strip().split(SEPARATOR)
            rule_map[int(parts[0])] = [convert(t) for t in tokens]
        else:
            received_messages.append(parts[0])

    return rule_map, received_messages


# Part One ---------------------------------------------------------------------


def graph_rules(rule_map: dict, rule_index: int) -> list[str]:
    """
    Graph all valid message rules

    :param rule_map: raw message rule map
    :param rule_index: rule map entry
    :return: list of valid message rules
    """

    rules = rule_map[rule_index]
    if isinstance(rules[0], str):
        return rules
    temp = list()
    retval = list()
    for r in rules:
        if r != '|':
            temp.append(graph_rules(rule_map, r))
        else:
            retval.extend(''.join(c) for c in itertools.product(*temp))
            temp = list()
    retval.extend(''.join(c) for c in itertools.product(*temp))

    return retval


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    rules, messages = decode(file=file)
    message_rules = set(graph_rules(rules, 0))
    if DEBUG:
        print(message_rules)

    valid_messages = sum(m in message_rules for m in messages)

    return valid_messages


# Part Two ---------------------------------------------------------------------


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    result: int = 0
    return result


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
    files = ['./example.txt']
    files = []
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
