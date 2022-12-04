import logging
import sys
import time
from math import prod
from pathlib import Path
from typing import Iterator
from common.support import configure_logger, parse_arguments

log = logging.getLogger(__name__)
EXIT_SUCCESS = 0


# Common Methods ---------------------------------------------------------------


ERROR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

OPENING_MAP = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

CLOSING_MAP = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

CLOSING_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def load_contents(filename: Path) -> Iterator[str]:
    """Load and convert contents from file

    :param filename: input filename
    :return: generator returning strings
    """
    with open(filename, encoding='utf-8') as buffer:
        for line in buffer.readlines():
            chunks = line.strip()
            yield chunks


def scan_syntax(line: str) -> Iterator[str]:
    """Scan the given line for syntax errors

    :param line: line with zero or more syntax errors
    :return: iterator over syntax errors
    """
    chunks = list()
    for chunk in line:
        opening_token = chunk in OPENING_MAP
        if opening_token:
            chunks.append(chunk)
        else:
            syntax_error = not CLOSING_MAP[chunk] == chunks.pop()
            if syntax_error:
                yield chunk


def solve_first_part(contents: Iterator[str]) -> int:
    """Solve the first part of the challenge

    :param contents:
    :return:
    """
    answer = 0
    for line in contents:
        for se in scan_syntax(line=line):
            answer += ERROR_SCORE[se]
            break
    return answer


def autocomplete(line: str) -> str:
    """Add closing characters in the correct order

    :param line: incomplete line
    :return: iterator over syntax errors
    """
    chunks = list()
    for chunk in line:
        opening_token = chunk in OPENING_MAP
        if opening_token:
            chunks.insert(0, OPENING_MAP[chunk])
        else:
            chunks.pop(0)
    return ''.join(chunks)


def solve_second_part(contents: Iterator[str]) -> int:
    """Solve the second part of the challenge

    :param contents:
    :return:
    """
    scores = list()
    for line in contents:
        corrupted_line = any(True for _ in scan_syntax(line=line))
        if corrupted_line:
            continue
        completion_string = autocomplete(line=line)
        score = 0
        for char in completion_string:
            score = 5 * score + CLOSING_SCORE[char]
        scores.append(score)
    scores.sort()
    answer = scores[len(scores) // 2]
    return answer


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """

    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'called with {args=}')

    start_time = time.perf_counter()

    contents = list(load_contents(filename=args.filename))
    compute_first_part = \
        'solve_first_part' in globals() and (not args.part or args.part == 1)
    compute_second_part = \
        'solve_second_part' in globals() and (not args.part or args.part == 2)
    answer_part_one = \
        solve_first_part(contents=contents) if compute_first_part else 0
    answer_part_two = \
        solve_second_part(contents=contents) if compute_second_part else 0

    elapsed_time = time.perf_counter() - start_time

    print(f'{answer_part_one=}')
    print(f'{answer_part_two=}')
    print(f'done in {1000 * elapsed_time:0.1f} milliseconds')

    return EXIT_SUCCESS


if __name__ == '__main__':
    if 1 == len(sys.argv):
        script_dir = Path(__file__).parent
        sys.argv.append(str(script_dir / 'example-input.txt'))
    sys.exit(main())
