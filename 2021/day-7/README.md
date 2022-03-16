Solution in [Python][py] for the [day 7 puzzle][aoc-2021-7] of the [2021 edition][aoc-2021] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 The Treachery of Whales 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?
> 
> There's one major catch - crab submarines can only move horizontally.

*Horizontally* they say? Should we be expecting part two to be on in two dimensions?

> You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.

Surely it must be harder than just computing the average?!

## 💾🔍 Content Decoding

> For example, consider the following horizontal positions:
> 
> ```
> 16,1,2,0,4,2,7,1,2,14
> ```

The content encoding is the [same as in day 6](../day-6/README.md#-content-decoding).

```python
def load_contents(filename: Path) -> [int]:
    """Load and convert contents from file

    :param filename: input filename
    :return: list of integers
    """
    with open(filename, encoding='utf-8') as buffer:
        line = next(iter(buffer.readlines()))
        tokens = [int(t) for t in line.strip().split(',')]
        return tokens
```

Hoping that `pylint` won't complain of code duplication.

## 💡🙋 Implementation

First thought was to compute an average. With the example input contents the average is `4.9` which is quite different from the correct answer `2`, meaning this first impression is invalid.

We could use successive guesses with a dichotomy, or some sort of converging offset. The starting point could be the most frequent number, and the initial direction the second most frequent.

The scanning algorithm which strongly looks like a [golden-section search][w-golden-section-search] will depend on the curve, more precisely if it is an [unimodal function][w-unimodal-function]. This function which computes the total fuel is easy:

```python
def compute_fuel_cost(h_positions: [int], h_position: int) -> int:
    """Compute fuel cost for a given configuration
    
    :param h_positions: list of initial horizontal positions
    :param h_position: final horizontal position
    :return: total fuel required for reaching final position
    """
    fuel = sum(abs(h_position - pos) for pos in h_positions)
    return fuel
```

On the example contents we obtain:

Position | Fuel
--- | ---
0 | 49
1 | 41
2 | 37
4 | 41
7 | 53
14 | 95
16 | 111

On the full input contents, we can simply sweep through all the positions and index the position by fuel cost:

```python
>>> map_ = {compute_fuel_cost(contents, pos): pos for pos in contents}
>>> map_[min(map_.keys())]
372
```

The complete method is straightforward:

```python
def solve_part_one(contents: any) -> int:
    """Solve the first part of the challenge

    :param contents: input puzzle contents
    :return: expected challenge answer
    """
    positions = sorted(set(contents))
    min_map = {compute_fuel_cost(contents, pos): pos for pos in positions}
    answer = min(min_map.keys())
    log.debug(f'Found min in listed positions: {answer}')
    return answer
```

Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day_7.py input.txt -p 1` | `337488` | 612.9 ms

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

> As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.

Meaning that instead of a linear function between the offset and the fuel cost, we now have a polynomial one.

## 🤔🤯 Puzzle Solver

Let's try the minimal effort first. The idea is to change as little as possible the `compute_fuel_cost()` method used in part one. The sum of integers from 0 to N is the same as the sum of integers from N to 0. Both have(N+1) members and because the sum N times (N+1) obviously being N*(N+1) we can affirm that the sum of 0 to N is N*(N+1)/2.

```python
def compute_fuel_cost_part_two(h_positions: [int], h_position: int) -> int:
    """Compute fuel cost for a given configuration
    
    :param h_positions: list of initial horizontal positions
    :param h_position: final horizontal position
    :return: total fuel required for reaching final position
    """
    fuel = sum(abs(h_position - pos)*(1+abs(h_position - pos))/2 for pos in h_positions)
    return fuel
```

Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day_7.py input.txt -p 2` | `89647695` | 1356.6 ms

We can feel there is quite some room for improvement, since the scanning method is very crude.

[aoc]: https://adventofcode.com/
[aoc-2021]: https://adventofcode.com/2021/
[aoc-2021-7]: https://adventofcode.com/2021/day/7
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

[w-golden-section-search]: https://en.wikipedia.org/wiki/Golden-section_search
[w-unimodal-function]: https://en.wikipedia.org/wiki/Unimodality#Unimodal_function
