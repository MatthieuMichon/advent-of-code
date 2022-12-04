import logging
import sys
import time
from pathlib import Path
from typing import Generator
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

PAIRS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}


def load_contents(filename: Path) -> Generator:
    """Load and convert contents from file

    :param filename: input filename
    :return: map generator
    """
    with open(filename, encoding='utf-8') as buffer:
        for line in buffer.readlines():
            chunks = line.strip()
            yield chunks


def scan_syntax(line) -> Generator:
    """Scan the given line for syntax errors

    :param line: line with zero or more syntax errors
    :return: iterator over syntax errors
    """
    chunks = list()
    for chunk in line:
        opening_token = chunk not in PAIRS
        if opening_token:
            chunks.append(chunk)
        else:
            syntax_error = not PAIRS[chunk] == chunks.pop()
            if syntax_error:
                yield chunk


def solve_first_part(contents: Generator) -> int:
    """Solve the first part of the challenge

    :param contents:
    :return:
    """
    answer = 0
    for line in contents:
        for se in scan_syntax(line):
            answer += ERROR_SCORE[se]
            break
    return answer


def main() -> int:
    """Script main method

    :return: script exit code returned to the shell
    """

    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    log.debug(f'called with {args=}')

    start_time = time.perf_counter()

    contents = load_contents(filename=args.filename)
    answer_part_one = solve_first_part(contents=contents) \
        if 'solve_first_part' in globals() else 0
    answer_part_two = solve_second_part(contents=contents) \
        if 'solve_second_part' in globals() else 0

    elapsed_time = time.perf_counter() - start_time

    print(f'{answer_part_one=}')
    print(f'{answer_part_two=}')
    print(f'done in {1000 * elapsed_time:0.1f} milliseconds')

    return EXIT_SUCCESS


if __name__ == '__main__':
    if 1 == len(sys.argv):
        script_dir = Path(__file__).parent
        sys.argv.append(str(script_dir / 'input.txt'))
    sys.exit(main())
