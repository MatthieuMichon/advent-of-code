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

    fp = open(file)
    convert = lambda t: int(t) if t.isnumeric() else t.replace('"', '')
    rule_map: dict[int, any] = dict()
    received_messages = list()
    for parts in (line.strip().split(RULE_NUMBER_SUFFIX) for line in open(file)):
        if len(parts) == 2:
            tokens = parts[1].strip().split(SEPARATOR)
            rule_map[int(parts[0])] = [convert(t) for t in tokens]
        else:
            if not len(parts[0]):
                continue
            received_messages.append(parts[0])

    return rule_map, received_messages


def graph_rules(rule_map: dict, rule_index: int) -> list[str]:
    """
    Graph all valid message rules

    :param rule_map: raw message rule map
    :param rule_index: rule map entry
    :param memoization:
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


# Part One ---------------------------------------------------------------------


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    rules, messages = decode(file=file)
    message_rules = set(graph_rules(rules, 0, {}))
    if DEBUG:
        print(message_rules)

    valid_messages = sum(m in message_rules for m in messages)

    return valid_messages


# Part Two ---------------------------------------------------------------------


def unroll(rules: dict[int, list], max_depth: int) -> dict[int, list]:
    """
    Unroll recursive rules at a max depth
    :param rules: rule map
    :param max_depth: max recursion depth
    :return: unrolled rule map
    """

    retval: dict[int, list] = dict()
    for k, v in rules.items():
        rule_is_recursive = k in v
        if rule_is_recursive:
            unrolled_rule = v[:v.index('|')]
            repeating_group = v[v.index('|')+1:]
            rule_suffix = repeating_group.copy()
            for depth in range(max_depth):
                i = rule_suffix.index(k)
                rule_suffix[i:i+1] = repeating_group
                unrolled_rule.extend(['|'] + rule_suffix)
            retval[k] = [item for item in unrolled_rule if item != k]
        else:
            retval[k] = v

    return retval


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    rules, messages = decode(file=file)

    # first attempt but way too compute intensive
    # max_msg_len = max(len(msg) for msg in messages)
    # rules[8] = [42, '|', 42, 8]
    # rules[11] = [42, 31, '|', 42, 11, 31]
    # rules = unroll(rules=rules, max_depth=max_msg_len)
    # message_rules = set(graph_rules(rules, 0))

    # solution copied from https://github.com/BastiHz/Advent_of_Code/blob/main/2020/day_19.py
    # rules 8 and 11 depend only on rules 31 and 42 which when graphed all have
    # the same length.

    rule_31_solutions = set(graph_rules(rules, 31))
    rule_31_sol_lengths = {len(s) for s in rule_31_solutions}
    rule_42_solutions = set(graph_rules(rules, 42))
    rule_42_sol_lengths = {len(s) for s in rule_42_solutions}
    assert rule_31_sol_lengths == rule_42_sol_lengths
    block_len = next(iter(rule_31_sol_lengths))

    valid_messages = 0
    for msg in messages:
        words = [msg[0 + i:block_len + i] for i in range(0, len(msg), block_len)]
        word_cnt = len(words)
        rule_31_match_cnt = 0
        for word in reversed(words):  # reverse since rule 31 matches at the end of message
            if word in rule_31_solutions:
                rule_31_match_cnt += 1
            else:
                break
        if 0 < rule_31_match_cnt < word_cnt/2 and all(word in rule_42_solutions for word in words[:-rule_31_match_cnt]):
            valid_messages += 1

    return valid_messages


# Main -------------------------------------------------------------------------


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    files = ['./example.txt', './input.txt']
    #files = ['./example.txt']
    files = []
    for f in files:
        print(f'In file {f}:')
        print(f'\tPart One: {process(file=Path(f))}')

    files = ['./example_part2.txt', './input.txt']
    #files = ['./input.txt']
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
