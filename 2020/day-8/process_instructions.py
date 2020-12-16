#!/usr/bin/env python
"""
Advent of Code 2020 - Day 7: Handy Haversacks
"""
import re
import sys
import copy
from pathlib import Path
from typing import List

INPUT_FILES = ['./short-input.txt', './input.txt']


def decode(file: Path) -> List:
    """
    Decode the given file

    :param file: file to process
    :return: string and int tuple
    """

    ret = list()
    for line in open(file):
        m = re.search(r'^(?P<op>\w{3}) (?P<arg>[+-]\d+)$', line)
        if not m:
            raise Exception(f'{line}')
        d = m.groupdict()
        ret.append([d['op'], int(d['arg'])])
    return ret


def execute(instruction: List) -> tuple:
    op, arg = instruction
    if op == 'nop':
        return 1, 0
    if op == 'jmp':
        return arg, 0
    if op == 'acc':
        return 1, arg


def process(file: Path) -> tuple[int, int]:
    """
    Process the given file

    :param file: custom declaration file to process
    :return: answer
    """

    instructions = decode(file=file)
    run_table = [{'instruction': i, 'visited': False} for i in instructions]
    pc = 0
    acc = 0
    index = 0
    while not run_table[pc]['visited']:
        pc_jump, acc_diff = execute(run_table[pc]['instruction'])
        run_table[pc]['visited'] = True
        index += 1
        pc += pc_jump
        acc += acc_diff

    print(f'Done after {index} steps')
    return index, acc


def process_part2(file: Path) -> int:
    """
    Process the given file

    :param file: custom declaration file to process
    :return: answer
    """

    instructions = decode(file=file)
    run_table = [{'instruction': i, 'visited': False} for i in instructions]
    temp_run_table = copy.deepcopy(run_table)
    pc = 0
    index = 1
    while not temp_run_table[pc]['visited']:
        pc_jump, acc_diff = execute(temp_run_table[pc]['instruction'])
        temp_run_table[pc]['visited'] = index
        pc += pc_jump
        index += 1

    max_subst_depth = index
    print(f'Max subst depth {max_subst_depth}')
    max_pc = 0
    for i in range(max_subst_depth):
        temp_run_table = copy.deepcopy(run_table)
        pc = 0
        acc = 0
        index = 0
        while pc < len(temp_run_table) and not temp_run_table[pc]['visited']:
            instruction = temp_run_table[pc]['instruction']
            if index == i:
                if instruction[0] == 'jmp':
                    instruction[0] = 'nop'
                elif instruction[0] == 'nop':
                    instruction[0] = 'jmp'
                else:
                    break
            pc_jump, acc_diff = execute(instruction)
            index += 1
            temp_run_table[pc]['visited'] = index
            pc += pc_jump
            if pc < 0:
                break
            max_pc = max(max_pc, pc)
            acc += acc_diff

        if pc >= len(run_table):
            print(f'## Swapped step {i}; executed {index} steps; PC: {pc}; acc: {acc}')
            break

    return acc


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    for file in INPUT_FILES:
        index, submission = process(file=Path(file))
        print(f'In file {file}, submission: {submission}')

    print('Part 2')

    for file in INPUT_FILES:
        submission = process_part2(file=Path(file))
        print(f'In file {file}, submission: {submission}')

    return 0


if __name__ == '__main__':
    """
    Command line entry-point
    """
    sys.exit(main())
