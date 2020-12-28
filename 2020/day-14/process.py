#!/usr/bin/env python
"""
Advent of Code 2020: Day 14
"""

import copy
import os
import re
import signal
import sys
from types import FrameType
from typing import List, Mapping
from pathlib import Path


TXT_FILES: List[Path] = [Path(f) for f in os.listdir('./') if '.txt' in f]
TXT_REGEX = re.compile(
    '(?P<item>\w+)(\[(?P<address>\d+)])?\s=\s(?P<value>\w+)')


def read_values(file: Path) -> Mapping:
    """
    Read netmask and memory values from an input file

    :param file: text file
    :return: generator of values formatted in a mapping
    """

    batch = dict()
    for i, l in enumerate(open(file)):
        m = TXT_REGEX.match(l)
        assert m, f'failed match on line {i}: {l}'
        if m['item'] == 'mask':
            if batch:
                yield batch
            value = m['value']
            mask: str = ''.join('1' if b == 'X' else '0' for b in value)
            overlay: str = ''.join('1' if b == '1' else '0' for b in value)
            batch['bitmask'] = int(mask, 2)
            batch['overlay'] = int(overlay, 2)
            batch['mem_values'] = dict()
        elif m['item'] == 'mem':
            address = int(m['address'], 10)
            value = int(m['value'], 10)
            batch['mem_values'][address] = value
        else:
            raise Exception(l)
    yield batch


def read_values_part2(file: Path) -> Mapping:
    """
    Read netmask and memory values from an input file

    :param file: text file
    :return: generator of values formatted in a mapping
    """

    batch = dict()
    for i, l in enumerate(open(file)):
        m = TXT_REGEX.match(l)
        assert m, f'failed match on line {i}: {l}'
        if m['item'] == 'mask':
            if batch:
                yield batch
            batch['mask'] = m['value']
            batch['mem_values'] = dict()
        elif m['item'] == 'mem':
            address = f'{int(m["address"], 10):036b}'
            value = int(m['value'], 10)
            batch['mem_values'][address] = value
        else:
            raise Exception(l)
    yield batch


def graph_addr_list(mask: str, index: int) -> List[int]:
    """
    Graph possible combinations of address with floating bit

    :param mask: mask encoded as a string or ['0', '1', 'X']
    :param index: mask bit index
    :return: list of possible matching addresses
    """

    #tree = list()
    if index == len(mask):
        return [int(mask, 2)]
    bit = mask[index]
    if bit != 'X':
        tree = graph_addr_list(mask=mask, index=1 + index)
    else:
        new_mask = list(mask)
        new_mask[index] = '0'
        new_str = ''.join(new_mask)
        tree = graph_addr_list(mask=new_str, index=1 + index)
        new_mask[index] = '1'
        new_str = ''.join(new_mask)
        tree.extend(graph_addr_list(mask=new_str, index=1 + index))
    return tree


def dump_batch(batch: Mapping) -> None:
    """
    Print batch contents

    :batch file: text file
    :return: nothing
    """

    print(f'Bitmask: {batch["bitmask"]:09x}, overlay: {batch["overlay"]:09x}')
    for k, v in batch['mem_values'].items():
        print(f'\t@0x{k:09x}: 0x{v:09x}')


def process(file: Path, part_two: bool = False) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :param part_two: true for processing part 2
    :return: value to submit
    """

    debug = False

    mem_map = dict()
    if not part_two:
        for batch in read_values(file=file):
            if debug:
                dump_batch(batch=batch)
            for addr, data in batch['mem_values'].items():
                updated_data = data & batch['bitmask'] | batch['overlay']
                mem_map[addr] = updated_data
    else:
        for batch in read_values_part2(file=file):
            mask = batch['mask']
            for addr, data in batch['mem_values'].items():
                masked_address = ''.join(
                    addr[i] if b == '0' else b for i, b in enumerate(mask))
                float_addresses = graph_addr_list(mask=masked_address, index=0)
                for address in float_addresses:
                    mem_map[address] = data

    submission = sum(mem_map.values())
    return submission


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    for file in TXT_FILES:
        submission = process(file=Path(file))
        print(f'In file {file}, submission: {submission}')

    print(f'Part 2')

    for file in TXT_FILES:
        submission = process(file=Path(file), part_two=True)
        print(f'In file {file}, submission: {submission}')

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


def install_signal_handler() -> None:
    """
    Install interrupt signal handler

    :return: nothing
    """

    signal.signal(signal.SIGINT, handle_sigint)


if __name__ == '__main__':
    install_signal_handler()
    sys.exit(main())
