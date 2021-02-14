#!/usr/bin/env python

import argparse
import logging
import os
import sys
from pathlib import Path


EXIT_SUCCESS = 0


def load_contents(filename: Path) -> list[int]:
    contents = list(map(int, open(filename).read().strip().split(os.linesep)))
    return contents


def main() -> int:
    parser = argparse.ArgumentParser()
    pa = parser.add_argument
    pa('filename', type=Path, help='input contents filename')
    pa('-v', '--verbose', action='store_true', help='print extra messages')
    args = parser.parse_args()
    verbose = args.verbose
    contents = load_contents(filename=Path(args.filename))
    answer = 0 #solve(contents=contents, verbose=verbose)
    if verbose:
        print(f'Day-1, file: {args.filename}')
    print(answer)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
