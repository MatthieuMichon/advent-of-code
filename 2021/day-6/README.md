Solution in [Python][py] for the [day 6 puzzle][aoc-2021-6] of the [2021 edition][aoc-2021] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Lanternfish 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> A massive school of glowing lanternfish swims past. They must spawn quickly to reach such large numbers - maybe exponentially quickly? You should model their growth rate to be sure.

The emphasis on the word *exponentially* is not innocent. We can expect some sort geometric list processing.

> Although you know nothing about this specific species of lanternfish, you make some guesses about their attributes. Surely, each lanternfish creates a new lanternfish once every 7 days.

The lanternfish's internal timer can be computed by doing a modulo of itself with `7`, however further down we have:

> The new lanternfish starts with an internal timer of 8 and does not start counting down until the next day.

This means that a modulo `7` will not work due to returning zero instead of seven. A solution would consist on using a classic method for updating the timer value:

```python
SPAWN_TIME = 7

def update_timer(timer: int) -> int:
    if timer == 0:
        timer = SPAWN_TIME
    timer -= 1
    return timer
```

> For example, suppose you were given the following list:
> 
> ```
> 3,4,3,1,2
> ```
> 
> This list means that the first fish has an internal timer of 3, the second fish has an internal timer of 4, and so on until the fifth fish, which has an internal timer of 2. Simulating these fish over several days would proceed as follows:
> 
> ```
> Initial state: 3,4,3,1,2
> After  1 day:  2,3,2,0,1
> After  2 days: 1,2,1,6,0,8
> After  3 days: 0,1,0,5,6,7,8
> After  4 days: 6,0,6,4,5,6,7,8,8
> After  5 days: 5,6,5,3,4,5,6,7,7,8
> After  6 days: 4,5,4,2,3,4,5,6,6,7
> After  7 days: 3,4,3,1,2,3,4,5,5,6
> After  8 days: 2,3,2,0,1,2,3,4,4,5
> After  9 days: 1,2,1,6,0,1,2,3,3,4,8
> After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
> After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
> After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
> After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
> After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
> After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
> After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
> After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
> After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
> ```

The iteration loop could be something like:

1. Count number of zeroed items
2. Update each item by decreasing its value by one a apply module seven
3. Append the counted number of times the number eight to the end of the list 

## 💾🔍 Content Decoding

The input contents are a comma separated list of integers.

```
3,4,3,1,2
```

The goal is to obtain a list:

```python
[3,4,3,1,2]
```

The corresponding method ending being one the simplest so far:

```python
def load_contents(filename: Path) -> [int]:
    """Load and convert contents from file

    :param filename: input filename
    :return: coordinates
    """
    with open(filename, encoding='utf-8') as buffer:
        line = next(iter(buffer.readlines()))
        tokens = [int(t) for t in line.strip().split(',')]
        return tokens
```

## 💡🙋 Implementation

The first part is straightforward to implement, especially with a inner method which makes things quite neat.

```python
def solve_part_one(contents: any) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    def update_timer(timer: int) -> int:
        if timer == 0:
            timer = SPAWN_TIME
        return timer - 1

    lanternfishs = contents.copy()
    for _ in range(1, DURATION + 1):
        respawned = sum(1 for timer in lanternfishs if timer == 0)
        lanternfishs = [update_timer(timer) for timer in lanternfishs]
        lanternfishs.extend([8] * respawned)
    answer = len(lanternfishs)
    return answer
```

Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day_6.py input.txt -p 1` | `362639` | 5229.7 ms

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

TBD

## 🤔🤯 Puzzle Solver

TBD

Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day_6.py input.txt -p 2` | `-` | - ms

[aoc]: https://adventofcode.com/
[aoc-2021]: https://adventofcode.com/2021/
[aoc-2021-6]: https://adventofcode.com/2021/day/6
[py]: https://docs.python.org/3/

[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-cmath]: https://docs.python.org/3/library/cmath.html
[py-copy]: https://docs.python.org/3/library/copy.html
[py-counter]: https://docs.python.org/3/library/collections.html#collections.Counter
[py-decimal]: https://docs.python.org/3/library/decimal.html
[py-dict]: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
[py-exit]: https://docs.python.org/3/library/sys.html?highlight=sys%20exit#sys.exit
[py-fractions]: https://docs.python.org/3/library/fractions.html
[py-generator]: https://docs.python.org/3/library/stdtypes.html#generator-types
[py-int]: https://docs.python.org/3/library/functions.html#int
[py-json-load]: https://docs.python.org/3/library/json.html#json.load
[py-iterator]: https://docs.python.org/3/reference/expressions.html#yield-expressions
[py-itertools]: https://docs.python.org/3/library/itertools.html
[py-itertools-permutations]: https://docs.python.org/3/library/itertools.html#itertools.permutations
[py-list]: https://docs.python.org/3/library/stdtypes.html#list
[py-main]: https://docs.python.org/3/library/__main__.html
[py-math]: https://docs.python.org/3/library/math.html
[py-math-comb]: https://docs.python.org/3/library/math.html#math.comb
[py-map]: https://docs.python.org/3/library/functions.html#map
[py-name]: https://docs.python.org/3/library/stdtypes.html#definition.__name__
[py-open]: https://docs.python.org/3/library/functions.html#open
[py-linesep]: https://docs.python.org/3/library/os.html#os.linesep
[py-read]: https://docs.python.org/3/library/io.html#io.TextIOBase.read
[py-readlines]: https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects
[py-return]: https://docs.python.org/3/reference/simple_stmts.html#the-return-statement
[py-set]: https://docs.python.org/3/library/stdtypes.html#set
[py-sn]: https://docs.python.org/3/library/types.html#types.SimpleNamespace
[py-split]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.split
[py-string]: https://docs.python.org/3/library/stdtypes.html#textseq
[py-strip]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
[py-sum]: https://docs.python.org/3/library/functions.html#sum
[py-tuple]: https://docs.python.org/3/library/stdtypes.html#tuple
[py-zip]: https://docs.python.org/3/library/functions.html#zip
