#!/usr/bin/env python

"""
Advent of Code day 22 challenge
"""

import os
import sys
from pathlib import Path


# Part One ---------------------------------------------------------------------


def print_part_one(files: list[str]) -> None:
    """Print submission results for part one

    :param files: list of files to process
    :return: nothing
    """

    for f in files:
        decks = read_decks(file=Path(f))
        round = 0
        while min(map(len, decks)):
            round += 1
            print(f'-- Round {round} --')
            print(f"Player 1's deck: {', '.join(map(str, decks[0]))}")
            print(f"Player 2's deck: {', '.join(map(str, decks[1]))}")
            decks = play_round(decks=decks)
            print('')
        print('== Post-game results ==')
        print(f"Player 1's deck: {', '.join(map(str, decks[0]))}")
        print(f"Player 2's deck: {', '.join(map(str, decks[1]))}")
        print('')
        winning_deck = max(decks, key=len)
        score = score_combat(deck=winning_deck)
        print(f'= {score}')


def play_round(decks: tuple[list[int]]) -> tuple[list[int]]:
    """Play a single round

    :param decks: deck for each players
    :return: updated deck for each players
    """

    top_cards = list(zip(*decks))[0]
    print(f'Player 1 plays: {top_cards[0]}')
    print(f'Player 2 plays: {top_cards[1]}')
    assert len(set(top_cards)) == 2
    decks = tuple(d[1:] for d in decks)
    winner = top_cards.index(max(card for card in top_cards))
    print(f'Player {1 + winner} wins the round!')
    top_cards = sorted(top_cards, reverse=True)
    decks[winner].extend(top_cards)
    return decks


# Part Two ---------------------------------------------------------------------


def print_part_two(files: list[str]) -> None:
    """Print submission results for part two

    :param files: list of files to process
    :return: nothing
    """

    for f in files:
        decks = read_decks(file=Path(f))
        decks = play_regular_combat(decks=decks)
        winning_deck = max(decks, key=len)
        score = score_combat(deck=winning_deck)
        print(f'= {score}')


def play_regular_combat(decks: tuple[list[int]]) -> tuple[list[int]]:
    """Play a single round

    :param decks: deck for each players
    :param game: recursive game level
    :return: updated deck for each players
    """

    game = 1
    print(f'=== Game {game} ===')
    print('')
    round = 0
    previous_decks = list()
    while min(map(len, decks)):
        if decks in previous_decks:
            assert False
        round += 1
        print(f'-- Round {round} (Game {game}) --')
        print(f"Player 1's deck: {', '.join(map(str, decks[0]))}")
        print(f"Player 2's deck: {', '.join(map(str, decks[1]))}")
        top_cards = list(zip(*decks))[0]
        print(f'Player 1 plays: {top_cards[0]}')
        print(f'Player 2 plays: {top_cards[1]}')
        assert len(set(top_cards)) == 2
        decks = tuple(d[1:] for d in decks)
        do_recursive_combat = all(len(d) >= top_cards[i]
                                  for i, d in enumerate(decks))
        if do_recursive_combat:
            print('Playing a sub-game to determine the winner...')
            print('')
            copied_decks = list()
            for i, deck in enumerate(decks):
                copied_decks.append(deck.copy()[:top_cards[i]])
            winner = play_recursive_combat(decks=tuple(copied_decks), game=game)
            print(f'...anyway, back to game {game}.')
        else:
            winner = top_cards.index(max(card for card in top_cards))
        print(f'Player {1 + winner} wins the round {round} of game {game}!')
        print('')
        top_cards = [top_cards[winner], top_cards[(1 + winner) % 2]]
        decks[winner].extend(top_cards)
    print('== Post-game results ==')
    print(f"Player 1's deck: {', '.join(map(str, decks[0]))}")
    print(f"Player 2's deck: {', '.join(map(str, decks[1]))}")
    print('')
    return decks


def play_recursive_combat(decks: tuple[list[int]], game: int) -> int:
    """Play a single round

    :param decks: deck for each players
    :param game: recursive game level
    :return: recursive combat game winner
    """

    game += 1
    print(f'=== Game {game} ===')
    round = 0
    winner = -1
    previous_decks = list()
    while min(map(len, decks)):
        if decks in previous_decks:
            return PLAYER_1
        previous_decks.append(decks)
        round += 1
        print('')
        print(f'-- Round {round} (Game {game}) --')
        print(f"Player 1's deck: {', '.join(map(str, decks[0]))}")
        print(f"Player 2's deck: {', '.join(map(str, decks[1]))}")
        top_cards = list(zip(*decks))[0]
        print(f'Player 1 plays: {top_cards[0]}')
        print(f'Player 2 plays: {top_cards[1]}')
        assert len(set(top_cards)) == 2
        decks = tuple(d[1:] for d in decks)
        do_recursive_combat = all(len(d) >= top_cards[i]
                                  for i, d in enumerate(decks))
        if do_recursive_combat:
            print('Playing a sub-game to determine the winner...')
            print('')
            copied_decks = list()
            for i, deck in enumerate(decks):
                copied_decks.append(deck.copy()[:top_cards[i]])
            winner = play_recursive_combat(decks=tuple(copied_decks), game=game)
        else:
            winner = top_cards.index(max(card for card in top_cards))
        print(f'Player {1 + winner} wins the round {round} of game {game}!')
        top_cards = sorted(top_cards, reverse=True)
        decks[winner].extend(top_cards)
    print(f'The winner of game {game} is player {1 + winner}!')
    print('')
    return winner


# Common -----------------------------------------------------------------------


PLAYER_1 = 0


def read_decks(file: Path) -> tuple[list[int]]:
    """Read decks from a file

    :param file: pathlib.Path file name
    :return: pair of decks (list of strings)
    """

    groups = open(file).read().split(2 * os.linesep)
    decks = tuple(list(map(int, g.splitlines()[1:])) for g in groups)
    return decks


def score_combat(deck: list[int]) -> int:
    """
    Score the winning deck

    :param deck: winning deck of cards
    :return: score
    """

    coefficient = len(deck)
    score = 0
    for card in deck:
        print(f'+ {card:2d} * {coefficient:2d}')
        score += coefficient * card
        coefficient -= 1
        if 0 == coefficient:
            break
    return score


def main() -> int:
    """Main function

    :return: shell exit code
    """

    files = ['./example.txt', './input.txt']
    #files = ['./example.txt']

    #print_part_one(files=files)
    print_part_two(files=files)

    return 0


if __name__ == '__main__':
    sys.exit(main())
