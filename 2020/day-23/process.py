import sys

from collections import deque


# Part One ---------------------------------------------------------------------


def print_part_one(inputs: list[dict[str, any]]) -> None:
    """Print answers for all the inputs of the part one

    :param inputs: puzzle input as a integer strings
    :return: nothing
    """
    for input_ in inputs:
        cups = decode_input(input_=input_['labels'])
        cups = mix_up(cups=cups, moves=input_['moves'])
        answer: int = compute_answer(cups=deque(cups))
        print(f'Puzzle part one answer is {answer}')


def mix_up(cups: list[int], moves: int, silent: bool = False) -> list[int]:
    """Mix up cups according to the challenge rules repeating a number of moves

    :param cups: list of digits
    :param moves: number of mixes
    :param silent: silence print messages
    :return: list of digits after mix up moves
    """
    for move in range(moves):
        print(f'-- move {1 + move} --')
        if not silent:
            print(f'cups: {dump_cups_with_first(cups)}')
        cups = move_cups(cups=cups, silent=silent)
        if not silent:
            print(' ')
    return cups


def move_cups(cups: list[int], silent: bool = False) -> list[int]:
    """Move cups following listed actions

    :param cups: list of digits
    :param silent: silence print messages
    :return: list of digits after completing required actions
    """
    def compute_destination_cup() -> int:
        destination_cup = current_cup - 1
        while destination_cup not in cups:
            destination_cup -= 1
            if destination_cup < min(cups):
                return max(cups)
        return destination_cup
    current_cup = cups[0]
    cw_cups = cups[1:4]
    if not silent:
        print(f"pick up: {', '.join(str(cup) for cup in cw_cups)}")
    del cups[1:4]
    cups = deque(cups)
    dest_cup = compute_destination_cup()
    if not silent:
        print(f'destination: {dest_cup}')
    cups.rotate(-cups.index(dest_cup))
    cups = list(cups)
    cups[1:1] = cw_cups
    cups = deque(cups)
    cups.rotate(-cups.index(current_cup)-1)
    return list(cups)


def dump_cups_with_first(cups: list[int]) -> str:
    """Dump list of cups with highlighting the first one

    :param cups: list of digits
    :return: list of cups in string format
    """
    dump_cup = lambda i, cup: f'({cup})' if i == 0 else f' {cup} '
    ret_val = ''.join([dump_cup(i, cup) for i, cup in enumerate(cups)])
    return ret_val


def compute_answer(cups: deque[int]) -> int:
    """Compute the answer of the part one

    :param cups: list of digits
    :return: part one answer
    """
    while cups[0] != 1:
        cups.rotate(-1)
    following_cups = list(cups)[1:]
    answer = int(''.join([str(cup) for cup in following_cups]))
    return answer


# Part One ---------------------------------------------------------------------


def print_part_two(inputs: list[dict[str, any]]) -> None:
    """Print answers for all the inputs of the part one

    :param inputs: puzzle input as a integer strings
    :return: nothing
    """
    for input_ in inputs:
        cups = decode_input(input_=input_['labels'])
        cups.extend(i for i in range(len(cups), 10**6))
        cups = mix_up(cups=cups, moves=input_['moves'], silent=True)
        answer: int = compute_answer_part_two(cups=deque(cups))
        print(f'Puzzle part one answer is {answer}')


def compute_answer_part_two(cups: deque[int]) -> int:
    """Compute the answer of the part two

    :param cups: list of digits
    :return: part one answer
    """
    while cups[0] != 1:
        cups.rotate(-1)
    following_cups = list(cups)[1:3]
    answer = int(following_cups[0]) * int(following_cups[1])
    return answer


# Common -----------------------------------------------------------------------


def decode_input(input_: str) -> list[int]:
    """Decode the puzzle input

    :param input_: puzzle input as a integer string
    :return: list of digits
    """
    cups = list(map(int, input_))
    assert len(cups) == len(set(cups))
    return cups


def main() -> int:
    """Main function

    :return: shell exit code
    """
    inputs = [
        {'labels': '389125467', 'moves': 10},
        {'labels': '389125467', 'moves': 100},
        {'labels': '963275481', 'moves': 100},
    ]
    print_part_one(inputs=inputs)
    inputs = [
        {'labels': '389125467', 'moves': 10**7},
        {'labels': '963275481', 'moves': 10**7},
    ]
    print_part_two(inputs=inputs)
    return 0


if __name__ == '__main__':
    sys.exit(main())
