#!/usr/bin/env python
"""
Advent of Code 2020: Day 16
"""

import math
import itertools
import re
import signal
import sys
from types import FrameType
from typing import List, Mapping, Dict
from pathlib import Path


DEBUG = False


def decode(file: Path) -> List:
    """
    Decode file contents

    :param file:
    :return: per-section mappings
    """

    fh = open(file)
    range_list = list()
    for l in fh:
        ranges_str = re.findall(r'(\d+-\d+)', l)
        if not ranges_str:
            yield range_list
            break
        ranges = [[int(n) for n in r.split('-')] for r in ranges_str]
        range_list.extend((range(*r) for r in ranges))

    values = list()
    for l in fh:
        if ',' in l:
            fields = [int(f) for f in l.strip().split(',')]
            values.append(fields)
        elif values:
            yield values
            values = list()

    yield values


def process(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    decoder = decode(file=file)
    ranges = next(decoder)
    sets = [set(range(r.start, 1 + r.stop)) for r in ranges]
    values = set.union(*sets)

    _ = next(decoder)  # skip my ticket

    nearby_tickets = next(decoder)

    invalid_values = (v for v in list(
        itertools.chain.from_iterable(nearby_tickets)) if v not in values)

    submission = sum(invalid_values)
    return submission


# Part Two


def decode_part2(file: Path) -> Mapping:
    """
    Decode file contents

    :param file:
    :return: per-section mappings
    """

    fh = open(file)

    incr_range_stop = lambda r: range(r.start, 1 + r.stop)
    set_from_field = lambda f: set(
        incr_range_stop(range(*[int(n) for n in f.split('-')])))
    fields = dict()
    field_regex = re.compile(
        r'(?P<key>[^:]+): (?P<lower>\S+) or (?P<upper>\S+)')
    for l in fh:
        m = field_regex.search(l)
        if not m:
            break
        sets = set.union(set_from_field(m['lower']), set_from_field(m['upper']))
        fields[m['key']] = sets

    tickets = list()
    for l in fh:
        if ':' in l:
            key = re.match(r'(?P<key>[^:]+)', l)['key']
            #tickets[key] = []
        elif ',' in l:
            ticket = [int(f) for f in l.strip().split(',')]
            tickets.append(ticket)
        else:
            my_ticket = ticket
            tickets = list()

    return {
        'fields': fields,
        'my_ticket': my_ticket,
        'nearby_tickets': tickets
    }


def process_part2(file: Path) -> int:
    """
    Process input file yielding the submission value

    :param file: file containing the input values
    :return: value to submit
    """

    data = decode_part2(file=file)
    valid_field_values = set.union(*list(data['fields'].values()))

    valid_tickets = list()
    for ticket in data['nearby_tickets']:
        if any(f not in valid_field_values for f in ticket):
            continue
        valid_tickets.append(ticket)
    valid_tickets.append(data['my_ticket'])

    values_per_col = list(zip(*valid_tickets))
    fields_per_col = list()
    cols_per_field = dict()
    for i, col in enumerate(values_per_col):
        fields_per_col.append([])
        for fname, fset in data['fields'].items():
            if all(value in fset for value in col):
                fields_per_col[-1].append(fname)
                if fname not in cols_per_field:
                    cols_per_field[fname] = [i]
                else:
                    cols_per_field[fname].append(i)
    sort_key = lambda x: len(x[1])
    constraints = sorted(cols_per_field.items(), key=sort_key)

    field_map: Dict[str, int] = dict()
    index_map: Dict[int, str] = dict()
    for fname, fcols in constraints:
        assert fname not in field_map
        assert not all(col in index_map for col in fcols)
        col = next(c for c in fcols if c not in index_map)
        index_map[col] = fname
        field_map[fname] = col

    submission = math.prod(data['my_ticket'][index] for name, index in field_map.items() if 'departure' in name)
    return submission


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    # files = ['./example.txt', './input.txt']
    # for f in files:
    #     print(f'In file {f}:')
    #     print(f'\tPart Two: {process_part2(file=Path(f))}')

    files = ['./example_part2.txt', './input.txt']
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
