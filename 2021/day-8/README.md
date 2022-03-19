Solution in [Python][py] for the [day 7 puzzle][aoc-2021-7] of the [2021 edition][aoc-2021] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 The Treachery of Whales 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.
> 
> For now, focus on the easy digits.
> 
> Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits.

First part covers digits with unambiguous number of segments. Let's do it.

Digit | Segments
--- | ---
`1` | 2
`4` | 4
`7` | 3
`8` | 7

## 💾🔍 Content Decoding

> Each entry consists of ten unique signal patterns, a `|` delimiter, and finally the four digit output value. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are).

First thing is to get a quick sense of scale from the contents file.

```python
len(open('2021/day-8/input.txt').readlines())
200
len(''.join(open('2021/day-8/input.txt').readlines()))
16906
```

So we have a 200 liner file with approx 17'000 characters, which is pretty much typical. Lets check that the pipe character appears exactly once per line.

```python
>>> all(1 == l.count('|') for l in open('2021/day-8/input.txt').readlines())
True
>>> all(2 == len(l.split('|')) for l in open('2021/day-8/input.txt').readlines())
True
```

Great this means we can break down each single line into two segments, respectively patterns and outputs.

```python
patterns, outputs = line.split('|')
```

Getting rid of extraneous chars and using lists instead of strings requires some sugar coating:

```python
patterns, outputs = [part.strip().split(' ') for part in line.split('|')]
```

Finishing things up, we will use an iterator meaning instead of returning the entire lists we yield each line at the time.




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
