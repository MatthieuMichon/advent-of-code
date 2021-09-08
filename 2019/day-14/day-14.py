#!/usr/bin/env python

"""Advent of Code Programming Puzzles

2019 Edition - Day 10
Puzzle Solution in Python
"""

import argparse
import logging
import math
import os
import sys

from collections import defaultdict
from pathlib import Path
from typing import Iterator

log = logging.getLogger(__name__)


# Common Methods ---------------------------------------------------------------


def load_contents(file: Path) -> Iterator[dict]:
    """Load and convert contents from a filename

    :param file: input file handle
    :return: iterator yielding a dict entry for each list of reactions
    """
    _ANSWER_PREFIX = '# ANSWER'
    _EQ_OPERATOR = ' => '
    _LHS_SEPARATOR = ', '
    _CHEM_SEPARATOR = ' '

    def split_lhs(lhs: str) -> Iterator:
        chems = lhs.split(_LHS_SEPARATOR)
        for chem in chems:
            yield split_chem(chem)

    def split_chem(chem: str) -> (int, str):
        qty, name = chem.split(_CHEM_SEPARATOR)
        qty = int(qty)
        return qty, name

    lines = open(file).read().split(os.linesep)
    log.info(f'Loaded {len(lines)} lines from {file=}')
    last_line_empty = lines[-1] == ''
    assert last_line_empty, f'Last line must be empty: "{lines[-1]}"'

    contents = dict()
    for line in lines:
        line_with_answer = _ANSWER_PREFIX in line
        if len(line):
            if not line_with_answer:
                lhs, rhs = line.split(_EQ_OPERATOR)
                lhs = tuple(split_lhs(lhs))
                rhs_qty, rhs_name = tuple(split_chem(rhs))
                contents[rhs_name] = {'lot': rhs_qty, 'chems': lhs}
            else:
                contents['answer'] = split_chem(line.split(_EQ_OPERATOR)[1])[0]
        else:
            yield contents
            contents = dict()


# Solving Methods --------------------------------------------------------------

def graph_ore_qty_old(contents: dict, chem_name: str) -> int:
    output_qty = contents[chem_name]['qty']
    input_chems = contents[chem_name]['lhs']
    ore_qty = 0
    for chem in input_chems:
        qty, name = chem
        if name == 'ORE':
            ore_qty += qty * math.ceil(qty / output_qty)
        else:
            ore_qty += graph_ore_qty_old(contents=contents, chem_name=name)
        log.debug(f'{chem_name=} -> {chem=} {ore_qty=}')
    return ore_qty


def do_bfs(chem_map: dict, fuel_qty: int = 1) -> int:
    """Execute a breadth-first search

    :param chem_map: chemical reactions map
    :param fuel_qty: number of FUEL units to produce
    :return: answer
    """
    reactions = list()
    reactions.append({'chem': 'FUEL', 'qty': fuel_qty})
    req_qty = defaultdict(int)
    ore_qty = 0
    while len(reactions):
        reaction = reactions.pop()
        chem_name = reaction['chem']
        if chem_name == 'ORE':
            ore_qty += reaction['qty']
        elif reaction['qty'] <= req_qty[chem_name]:
            req_qty[chem_name] -= reaction['qty']
        else:
            qty_required = reaction['qty'] - req_qty[chem_name]
            new_reaction = chem_map[chem_name]
            lots = math.ceil(qty_required / new_reaction['lot'])
            for lhs_chem in new_reaction['chems']:
                reactions.append({'chem': lhs_chem[1], 'qty': lots * lhs_chem[0]})
            qty_extra = lots * new_reaction['lot'] - qty_required
            req_qty[chem_name] = qty_extra
    return ore_qty


def solve_part_one(reactions: dict) -> int:
    """Provide answer for part one of the puzzle

    :param reactions: mapping of chemical reactions
    :return: answer of part one
    """

    answer = do_bfs(chem_map=reactions)
    return answer


# Support Methods --------------------------------------------------------------


EXIT_SUCCESS = 0
EXIT_ERROR = 1
LOG_FORMAT = '# %(msecs)-3d - %(funcName)-16s - %(levelname)-8s - %(message)s'


def configure_logger(verbose: bool) -> None:
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
    """Main method

    :return: shell exit code
    """
    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'Arguments: {args}')
    compute_part_one = not args.part or 1 == args.part
    compute_part_two = not args.part or 2 == args.part
    if compute_part_one:
        for reactions in load_contents(file=Path(args.filename)):
            expected_answer = None
            if 'answer' in reactions:
                expected_answer = reactions.pop('answer')
            answer = solve_part_one(reactions=reactions)
            if expected_answer:
                assert expected_answer == answer, \
                        f'{expected_answer=} vs {answer=}'
            else:
                print(f'part one: answer: {answer}')
    if compute_part_two:
        return EXIT_ERROR
        print(f'part two: answer: {answer}')
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
