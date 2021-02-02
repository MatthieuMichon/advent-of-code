# Day 23: Crub Cups

[Challenge statement][d23-challenge] - 

# Challenge Review

> The cups will be arranged in a circle and labeled clockwise (your puzzle input).

Circular lists are likely to be used. A quick search on `python circular list` yields the following suggestions for data structures relevant to this application.

Type | Direct Access | Circular Access | Slice Access | Sequence Length
--- | --- | --- | --- | ---
[`list`][py-list] | Yes | No | Yes | Yes
[`collections.deque`][py-collections-deque] | Yes | Yes | With casting | Yes
[`itertools.cycle`][py-itertools-cycle] | No | Yes | No | No

The cups are arranged in a clockwise fashion, meaning iterating through them requires selecting the next cup on the right. The [`collections.deque`][py-collections-deque] type provides a [`rotate()`][py-collections-deque-rotate] method which when given an argument value of `-1` will rotate the cotents such as the next item on the right becomes the first one.

> Each move, the crab does the following actions:

A series of actions are to be executed sequentially in what is referred as a *move*. This action is repeated a number of times, up to one hundred.

> * The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.

Employed verbs: *picks*; *removed*; *adjusted*.

Moving the selected cups into a separate store may be required.

> * The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.

Employed verbs: *selects*.

Some additional logic is required for handling fallback scenarios:

* Keep subtracting one until it finds a cup that wasn't just picked up.
* If below the lowest value, it wraps around to the highest value.

> * The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.

Employed verbs: *places*.

The synonym *inserts* appears to better describe the operation.

> * The crab selects a new current cup: the cup which is immediately clockwise of the current cup.

Employed verbs: *selects*.

Enumerated verbs: *picks*; *removed*; *adjusted*; *selects*; *inserts*.

# Puzzle Input Handling

> The cups will be arranged in a circle and labeled clockwise.

The list of cups is encoded in an integer composed by a number of distinct digits.

Input decoding consists in converting a string representing an integer into a list of digits.

1. Convert the string into a sequence of chars. The [`tuple`][py-tuple] is used since this variable will not be changed.
1. Convert each item of the sequence into a single-digit integer.

```python
input_: str = '389125467'
cups: list[int] = tuple(map(int, input_))
```

Note: An assertion must be used for ensuring all items have a different digit.

```python
assert len(cups) == len(set(cups))
```

The complete input decoding function:
 
```python
def decode_input(input_:str) -> itertools.cycle:
    digits: tuple[int] = tuple(int(d) for d in input_)
    assert len(list(digits)) == len(set(digits))
    cups = itertools.cycle(digits)
    return cups
```

The [`itertools.cycle`][py-itertools-cycle] method is used with the belief that the returned object may provide useful methods.

# Challenge Part One

Part one relies on two stages:

1. Number of iterations.
2. Submission value computation.

## Iterative Processing Implementation

The number of iterations is defined in the challenge as `100`.

In prevision of the second part, these iterations are handled by two functions for better re-usability.

* A first method `mix_up()` called directly from `print_part_one()`.
* A second method `iterate()` which applies the series of actions on the list of cups.

The first method receives the initial cups arrangement and the number of iterations to perform.

```python
def mix_up(cups: deque[int], moves: int) -> deque[int]:
    for move in range(moves):
        cups = move_cups(cups=cups)
    return cups
```

The second method contains most of the processing:

> The crab picks up the three cups that are immediately clockwise of the current cup.

The three clockwise cups are copied in a `cw_cups`.

```python
cw_cups = cups[1:4].copy()
```

> They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.

```python
del cups[1:4]
cups = deque(cups)
```

> The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.

The logic for implementing this action consists in a selection followed by a loop and an exit condition for the wrapping.

```python
# Note: following is a nested impure function
def compute_destination_cup() -> int:
    destination_cup = current_cup - 1
    while destination_cup not in cups:
        destination_cup -= 1
        if destination_cup < min(cups):
            return max(cups)
    return destination_cup
```

> The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.

This action is implemented using a loop and a slice insertion. There is likely a better implementation without having to convert between `deque` and `list`.

```python
while cups[0] != destination_cup:
    cups.rotate(-1)
cups = list(cups)
cups[1:1] = cw_cups
cups = deque(cups)
```

> The crab selects a new current cup: the cup which is immediately clockwise of the current cup.

Also a loop for repositioning the cups bringing the new current cup in first position.

```python
while cups[0] != current_cup:
    cups.rotate(-1)
cups.rotate(-1)
```

The complete function:

```python
def move_cups(cups: deque[int]) -> deque[int]:
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
    del cups[1:4]
    cups = deque(cups)
    destination_cup = compute_destination_cup()
    while cups[0] != destination_cup:
        cups.rotate(-1)
    cups = list(cups)
    cups[1:1] = cw_cups
    cups = deque(cups)
    while cups[0] != current_cup:
        cups.rotate(-1)
    cups.rotate(-1)
    return cups
```

## Submission Value Computation

> What are the labels on the cups after cup 1?

Returning the labels on the remaining cups requires:

* Rotating the list of cups until the current cup label matches the value `1`.

```python
while cups[0] != 1:
    cups.rotate(-1)
```

* Copying a slice of all the cups but the first one using `[:1]`.

```python
following_cups = cups[1:]
```

* Convert to a string each of the items of the new slice.
* Merging together these string items into a single string using.
* Converting this string back to a multiple digit integer.

```python
answer = int(''.join([str(cup) for cup in following_cups]))
```

The complete function being:

```python
def compute_answer(cups: deque[int]) -> int:
    while cups[0] != 1:
        cups.rotate(-1)
    following_cups = list(cups)[1:]
    answer = int(''.join([str(cup) for cup in following_cups]))
    return answer
```

# Part Two

## Puzzle Input Decoding

Second part of the challenge starts by increasing the number of cups to one million.

> the crab starts arranging many cups in a circle on your raft - one million (1000000) in total.

The `decode_input()` method will definitively have to updated for providing these extra cups.

> Your labeling is still correct for the first few cups; after that, the remaining cups are just numbered in an increasing fashion starting from the number after the highest number in your list and proceeding one by one until one million is reached.

The extra cups can be added using a list comprehension.

```python
cups.extend(i for i in range(len(cups), 10**6))
```

The function thus becomes:

```python

```

## Iterative Processing Implementation

> the crab is going to do ten million (10000000) moves!

The number of iteration must be bumped from one hundred to ten million, which requires an efficient implementation.

The critical path in the implementation for part one goes through two loops, which must be replaced with something more efficient.

```python
# portion of the slow code
while cups[0] != destination_cup:
    cups.rotate(-1)
cups = list(cups)
cups[1:1] = cw_cups
cups = deque(cups)
while cups[0] != current_cup:
    cups.rotate(-1)
```

Speed was improved about ten fold.

```python
# portion with the updated code
    cups.rotate(-cups.index(destination_cup))
    cups = list(cups)
    cups[1:1] = cw_cups
    cups = deque(cups)
    cups.rotate(-cups.index(current_cup))
```

However this is far from being enough optimized for the answer to be computed in seconds. The code was further optimized by getting rid of costly conversions between [`list`][py-list] and [`collections.deque`][py-collections-deque] types, leaving the following method.

```python
def move_cups_deque(cups: deque[int], silent: bool = False) -> deque[int]:
    def compute_destination_cup() -> int:
        destination_cup = current_cup - 1
        while destination_cup not in cups:
            destination_cup -= 1
            if destination_cup < min(cups):
                return max(cups)
        return destination_cup
    current_cup = cups[0]
    cups.rotate(-1)
    cw_cups = list()
    for i in range(3):
        cw_cups.append(cups.popleft())
    dest_cup = compute_destination_cup()
    cups_len = len(cups)
    cups.rotate(cups_len-cups.index(dest_cup))
    for i, c in enumerate(cw_cups):
        cups.insert(1 + i, c)
    cups.rotate(-cups.index(current_cup)-1)
    return cups
```

However the speed-up while significant is far from enough for computing 10**7 moves. This suggests that the [`collections.deque`][py-collections-deque] may not be suited for working with such large data set.

Using an implementation relying on a [`list`][py-list] type yielded a further improvement, but falls still short of an acceptable target. 

```python
def move_cups_list(cups: list[int], cups_len: int) -> list[int]:
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
```

Looking at the big picture, it appears that assuming the `destination_cup_label` is not in part of the `picked_cups` list of integers, which is nearly always the case with 10^6 cups. If so there could be a way to optimize with, instead of having the `current_cup` always as a first item, having the list fixed and moving the index of the `current_cup` along the list.

```
odds = (10^6 - 3 - 1) / (10^6 - 1)
```

## Submission Value Computation

> Determine which two cups will end up immediately clockwise of cup 1. What do you get if you multiply their labels together?

```python
def compute_answer_part_two(cups: deque[int]) -> int:
    while cups[0] != 1:
        cups.rotate(-1)
    following_cups = list(cups)[1:3]
    answer = int(following_cups[0]) * int(following_cups[1])
    return answer

```
# Summary

* Input handling: simple and happy with the implementation.
* Part one
    * Iterative computation: simple but many type changes between `list` and `deque`, leaving room for improvement.
    * Puzzle value computation: simple and happy with the implementation.

[d23-challenge]: https://adventofcode.com/2020/day/23
[py-list]: https://docs.python.org/3/library/stdtypes.html?highlight=list#list
[py-tuple]: https://docs.python.org/3/library/stdtypes.html?highlight=tuple#tuple
[py-collections-deque]: https://docs.python.org/3/library/collections.html?highlight=deque#collections.deque
[py-collections-deque-rotate]: https://docs.python.org/3/library/collections.html?highlight=deque#collections.deque.rotate
[py-itertools-cycle]: https://docs.python.org/3/library/itertools.html?highlight=cycle#itertools.cycle
