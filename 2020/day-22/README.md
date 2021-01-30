# Day 22: Crab Combat

Relevant challenge statement:

> the game consists of a series of rounds: both players draw their top card, and the player with the higher-valued card wins the round. The winner keeps both cards, placing them on the bottom of their own deck so that the winner's card is above the other card. If this causes a player to have all of the cards, they win, and the game ends.

# Submission Implementation

## Content Decoding

Relevant submission extract:

> the cards so each player has their own deck

Content analysis shows that files are split in lines according the new line character as support by the operating system.

1. Read the given file completely.
1. Split the string on two consecutive new-line chars into groups.
1. For each group:
    1. Split on new-line chars.
    1. Discard the first item ``Player x:``

```
Step 1: 'Player 1:\n9\n2\n6\n3\n1\n\nPlayer 2:\n5\n8\n4\n7\n10\n'
Step 2: ['Player 1:\n9\n2\n6\n3\n1, Player 2:\n5\n8\n4\n7\n10\n']
Step 3.1: (['Player 1:', '9', '2', '6', '3', '1'], ['Player 2:', '5', '8', '4', '7', '10'])
Step 3.2: (['9', '2', '6', '3', '1'], ['5', '8', '4', '7', '10'])
```

Source code:

```python
def read_decks(file: Path) -> tuple[list[str]]:
    groups = open(file).read().split(2 * os.linesep)
    decks = tuple(g.splitlines()[1:] for g in groups)
    return decks
```

## Iteration Looping

1. Start with both decks.
1. Both players draw their top card.
1. The player with the higher-valued card wins the round.
1. The winner keeps both cards.
1. The winner places the cards them on the bottom of their own deck, so that the winner's card is above the other card.

```
-- Round x --
Step 1: Player 1's deck: 9, 2, 6, 3, 1
        Player 2's deck: 5, 8, 4, 7, 10
Step 2: Player 1 plays: 9
        Player 2 plays: 5
Step 3: Player 1 wins the round!
Step 4: Player 1 keeps ['9', '5']
Step 5: Player 1's deck: 2, 6, 3, 1, 9, 5
        Player 2's deck: 8, 4, 7, 10
```

Source code:

```python
def play_round(decks: tuple[list[str]]) -> tuple[list[str]]:
    top_cards = list(zip(*decks))[0]
    decks = tuple(d[1:] for d in decks)
    winner = top_cards.index(max(card for card in top_cards))
    top_cards = sorted(top_cards, reverse=True)
    decks[winner].extend(top_cards)
    return decks
```

Exit condition: one of the player has **all of the cards**.

```python
while min(map(len, decks)):
```

### Submission Computation

Relevant challenge extract:

> The bottom card in their deck is worth the value of the card multiplied by 1, the second-from-the-bottom card is worth the value of the card multiplied by 2, and so on. With 10 cards, the top card is worth the value on the card multiplied by 10.

The corresponding operations being:

* Set the coefficient with the deck length and clear the accumulator value.
* For each card:
    1. Multiply with the coefficient and accumulate.
    1. Decrement the accumulator.
    1. Break if accumulator is zero.

```python
def score_combat(deck: list[int]) -> int:
    coefficient = len(deck)
    score = 0
    for card in deck:
        print(f'+ {card:2d} * {coefficient:2d}')
        score += coefficient * card
        coefficient -= 1
        if 0 == coefficient:
            break
    return score
```

## Part Two

The challenge is altered by adding a number of rules governing how rounds are conducted.

> Before either player deals a card, if there was a previous round in this game that had exactly the same cards in the same order in the same players' decks, the game instantly ends in a win for player 1. Previous rounds from other games are not considered.

If the current deck configuration was already encountered in past then the game ends and player 1 wins.

> If both players have at least as many cards remaining in their deck as the value of the card they just drew, the winner of the round is determined by playing a new game of Recursive Combat.

Due to recursion, it makes sense to factorize the method which takes in input both decks and runs iterations until an exit condition is found.
