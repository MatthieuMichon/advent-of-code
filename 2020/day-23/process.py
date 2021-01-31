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
        answer: int = compute_answer(cups=cups)
        print(f'Puzzle part one answer is {answer}')


def mix_up(cups: deque[int], moves: int) -> deque[int]:
    """Mix up cups according to the challenge rules repeating a number of moves

    :param cups: list of digits
    :param moves: number of mixes
    :return: list of digits after mix up moves
    """

    for move in range(moves):
        print(f'-- move {1 + move} --')
        print(f'cups: {dump_cups_with_first(cups)}')
        cups = move_cups(cups=cups)
        print(' ')
    return cups


def move_cups(cups: deque[int]) -> deque[int]:
    """Move cups following listed actions

    :param cups: list of digits
    :return: list of digits after completing required actions
    """
    def compute_destination_cup() -> int:
        destination_cup = current_cup - 1
        while destination_cup not in cups:
            destination_cup -= 1
            if destination_cup < min(cups):
                return max(cups)
        return destination_cup
    cups = list(cups)
    current_cup = cups[0]
    cw_cups = cups[1:4].copy()
    print(f"pick up: {', '.join(str(cup) for cup in cw_cups)}")
    del cups[1:4]
    cups = deque(cups)
    destination_cup = compute_destination_cup()
    print(f'destination: {destination_cup}')
    while cups[0] != destination_cup:
        cups.rotate(-1)
    cups = list(cups)
    cups[1:1] = cw_cups
    cups = deque(cups)
    while cups[0] != current_cup:
        cups.rotate(-1)
    cups.rotate(-1)
    return cups


def dump_cups_with_first(cups: deque[int]) -> str:
    """
    Dump list of cups with highlighting the first one

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


# Common -----------------------------------------------------------------------


def decode_input(input_:str) -> deque[int]:
    """Decode the puzzle input

    :param input_: puzzle input as a integer string
    :return: list of digits
    """
    cups = deque(map(int, input_))
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

    return 0


if __name__ == '__main__':
    sys.exit(main())
