#!/usr/bin/env python
"""
Advent of Code 2020 - Day 7: Handy Haversacks
"""
import re
import sys
from pathlib import Path

INPUT_FILES = ['./short-input.txt', './input.txt']


def graph_node(contents_per_bag, bag_list):
    bag_graph = {}
    for bag in bag_list:
        bag_graph[bag] = graph_node(contents_per_bag, contents_per_bag[bag])
    return bag_graph


def decode(line: str, track_qty: bool = False) -> tuple:
    """
    Decode file line

    :param line: line string
    :param track_qty: duplicate bags depending on quantity
    :return: luggage properties
    """

    line = re.sub(r' bags?', '', line.strip().replace('.', ''))
    m = re.match(r'(?P<bag>.+?) contain (?P<contents>.+)', line)
    assert m
    bag = m.groupdict()['bag']
    contents = list()
    for item in m.groupdict()['contents'].split(', '):
        m = re.match(r'(?P<qty>\d+) (?P<inner_bag>.+)', item)
        if not m:
            continue
        inner_bag = m.groupdict()['inner_bag']
        qty = m.groupdict()['qty']
        if not track_qty:
            contents.extend([inner_bag])
        else:
            contents.extend([inner_bag] * int(qty))
    return bag, contents


def search_recursive(graph_per_bag, bag, target) -> bool:
    if not graph_per_bag[bag]:
        return False
    if target in graph_per_bag[bag]:
        return True
    for b in graph_per_bag[bag]:
        ret = search_recursive(graph_per_bag, b, target)
        if ret:
            return True
    return False


def count_recursive(contents_per_bag, bag_list):
    """
    Count number of nested bags from the given list

    :param contents_per_bag: per-bag mapping
    :param bag_list: list of bag to inspect
    :return: number of bags
    """

    nested_bag_qty = 0
    for bag in bag_list:
        nested_bag_qty += 1
        nested_bag_qty += count_recursive(contents_per_bag, contents_per_bag[bag])
    return nested_bag_qty


def process(file: Path) -> int:
    """
    Process the given file

    :param file: custom declaration file to process
    :return: answer
    """

    decoded_lines = [decode(line) for line in open(file=file)]
    contents_per_bag = {k: v for k, v in decoded_lines}
    bag_list = contents_per_bag.keys()
    bag_colors_qty = sum(
        search_recursive(contents_per_bag, bag, 'shiny gold') for bag in bag_list)

    return bag_colors_qty


def process_part2(file: Path) -> int:
    """
    Process the given file

    :param file: custom declaration file to process
    :return: answer
    """

    decoded_lines = [decode(line, track_qty=True) for line in open(file=file)]
    contents_per_bag = {k: v for k, v in decoded_lines}
    bag_qty = count_recursive(contents_per_bag, ['shiny gold']) - 1

    return bag_qty


def main() -> int:
    """
    Main function

    :return: Shell exit code
    """

    for file in INPUT_FILES:
        submission = process(file=Path(file))
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
