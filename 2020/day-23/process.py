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
        cups_list = mix_up_static(cups=cups, moves=input_['moves'])
        answer: int = compute_answer(cups=deque(cups_list))
        print(f'Puzzle part one answer is {answer}')


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


# Part Two ---------------------------------------------------------------------


def print_part_two(inputs: list[dict[str, any]]) -> None:
    """Print answers for all the inputs of the part one

    :param inputs: puzzle input as a integer strings
    :return: nothing
    """
    for input_ in inputs:
        cups = decode_input(input_=input_['labels'])
        cups.extend(1 + i for i in range(len(cups), 10**6))
        cups = mix_up_static(cups=cups, moves=input_['moves'])
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


def mix_up_list(cups: list[int], moves: int, silent: bool = False) -> list[int]:
    """Mix up cups according to the challenge rules repeating a number of moves

    :param cups: list of digits
    :param moves: number of mixes
    :param silent: silence print messages
    :return: list of digits after mix up moves
    """
    cups_len = len(cups)
    for move in range(moves):
        if not move % 100:
            print(f'-- move {1 + move} --')
        cups = move_cups_list(cups=cups, cups_len=cups_len)
    cups = list(cups)
    return cups


def move_cups_list(cups: list[int], cups_len: int) -> list[int]:
    """Move cups following listed actions

    :param cups: list of digits
    :param cups_len: length of cup list
    :return: list of digits after completing required actions
    """
    picked_cups = cups[0:4]
    destination_cup_label = picked_cups[0] - 1
    while (destination_cup_label in picked_cups[1:4]) \
            or (destination_cup_label == 0):
        destination_cup_label = (destination_cup_label - 1) % (1 + cups_len)
    destination_cup_index = 1 + cups.index(destination_cup_label)
    cups[destination_cup_index:destination_cup_index] = picked_cups[1:4]
    cups.append(cups[0])
    cups = cups[4:]
    return cups


def mix_up_static(cups: list[int], moves: int) -> list[int]:
    """Mix up cups according to the challenge rules repeating a number of moves

    :param cups: list of digits
    :param moves: number of mixes
    :return: list of digits after mix up moves
    """
    cups_len = len(cups)
    index = 0
    for move in range(moves):
        rollover = 4 + index > cups_len
        if not rollover:
            picked_cups = cups[1 + index:4 + index]
        else:
            for i in range(3):
                picked_cups[i] = cups[(i + 1 + index) % cups_len]
        destination_cup_label = cups[index % cups_len] - 1
        while (destination_cup_label in picked_cups) \
                or (destination_cup_label == 0)\
                or ((destination_cup_label < 10) and destination_cup_label not in cups):
            destination_cup_label = (destination_cup_label - 1) % (1 + cups_len)
        destination_cup_index = 1 + cups.index(destination_cup_label)
        rollover = destination_cup_index < 4 + index
        if not rollover:
            cups[index + 1:destination_cup_index - 3] = cups[index + 4:destination_cup_index]
            cups[destination_cup_index - 3:destination_cup_index] = picked_cups
        else:
            for i in range(index + 1, cups_len + destination_cup_index - 3):
                cups[i % cups_len] = cups[(i + 3) % cups_len]
            for i in range(cups_len + destination_cup_index - 3, cups_len + destination_cup_index):
                cups[i % cups_len] = picked_cups[i - (cups_len + destination_cup_index - 3)]
        index = (index + 1) % cups_len
    return cups


def dump_cups_with_first(cups: list[int]) -> str:
    """Dump list of cups with highlighting the first one

    :param cups: list of digits
    :return: list of cups in string format
    """
    dump_cup = lambda i, cup: f'({cup})' if i == 0 else f' {cup} '
    ret_val = ''.join([dump_cup(i, cup) for i, cup in enumerate(cups)])
    return ret_val


def main() -> int:
    """Main function

    :return: shell exit code
    """
    inputs = [
        #{'labels': '12345', 'moves': 1},
        #{'labels': '38915426', 'moves': 10},
        {'labels': '389125467', 'moves': 10},
        {'labels': '389125467', 'moves': 100},
        {'labels': '963275481', 'moves': 100},
    ]
    #print_part_one(inputs=inputs)
    inputs = [
        {'labels': '389125467', 'moves': 10**7},
        {'labels': '963275481', 'moves': 10**7},
    ]
    print_part_two(inputs=inputs)
    return 0


if __name__ == '__main__':
    sys.exit(main())
