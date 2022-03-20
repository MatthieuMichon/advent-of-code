Solution in [Python][py] for the [day 3 puzzle][aoc-2021-3] of the [2021 edition][aoc-2021] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Binary Diagnostic 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell you many useful things about the conditions of the submarine. The first parameter to check is the **power consumption**.

Expect a list of binary numbers as the input contents for this puzzle.

Several parameters (per-line maybe), with the first one being the power consumption (which appears to be variable ?).

> You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

So one (or more ?) binary are used for computing the two rates which are in turn multiplied giving us the power consumption.

> Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report.

> :memo: Note:
> 
> Check C1: all the binary number to be the same length.

Obvious way for computing the *gamma rate* is for each bit index (i.e. character column) compare the number of occurrences of `1` against `0` and keep the highest one. 

> The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Same as before using the opposite comparison.

> Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)

Good point regarding the binary to decimal conversion. The smartest method would be to compute both rates as integers.

## 💾🔍 Content Decoding

First, let's confirm the check C1:

```python
from collections import Counter

line_lengths = []
for line in open('./advent-of-code/2021/day-3/input.txt').readlines():
    line_lengths.append(len(line))
assert len(Counter(line_lengths)) == 1
```

Thankfully this check passes.

Looking at the part one statement, returning a list of bits of each index would be convenient. However, the second part of this challenge may require using the original contents (instead of the rotated array). Therefore it would be safer to just return an [iterator](py-iterator) and let the higher level methods deal with the format.

Each line holding a number of chars, using a [tuple](py-tuple) for each line is the logical choice hence the `Iterator[tuple]` returned object.

```python
def load_contents(filename: Path) -> Iterator[tuple]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator
    """
    ...
```

A loop runs over each line of the file:

```python
for line in open(filename).readlines():
    ...
```

At this point we are offered two solutions:

1. split each line in a tuple of `0` or `1` chars
2. convert each line to a binary integer with the [`int()`](py-int) method

The first solution seems more fun, although the second may perform better by avoiding a per-bit type conversion. So let's try the first solution and see how it fares.

```python
yield tuple(line)
```

The complete `load_contents()` ending up being:

```python
def load_contents(filename: Path) -> Iterator[tuple]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator
    """
    for line in open(filename).readlines():
        yield tuple(line.strip())
    log.debug(f'Reached end of {filename=}')
```

A quick check shows extra line return chars ending up caught in the tuple. This is easily solved by stripping with the [`strip()`](py-strip) method.

## 💡🙋 Implementation

First operation consists in rotating the two dimensional array using [`zip`](py-zip). Doing so allows us to access to the list of bits on a per bit index basis.

Next step is only a matter in iterating over each bit index an computing which of the `0` or `1` has the most and least occurrences.

```python
def solve_part_one(diagnostic_report: Iterator[tuple]) -> int:
    """Solve the first part of the challenge

    :param diagnostic_report: binary numbers
    :return: expected challenge answer
    """
    diagnostic_report = tuple(zip(*diagnostic_report))
    gamma_rate = ''
    epsilon_rate = ''
    for bits in diagnostic_report:
        values = Counter(bits)
        gamma_rate += str(values.most_common()[0][0])
        epsilon_rate += str(values.most_common()[1][0])
    gamma_rate = int(gamma_rate, 2)
    epsilon_rate = int(epsilon_rate, 2)
    answer = gamma_rate * epsilon_rate
    return answer
```

Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day_3.py input.txt -p 1` | `852500` | 24.4 ms

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

> Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating by the CO2 scrubber rating.

Two new variables are added to the mix.

```python
def solve_part_two(diagnostic_report: Iterator[tuple]) -> int:
    ...
    answer = oxygen_generator_rating * co2_scrubber_rating
    return answer
```

> Before searching for either rating value, start with the full list of binary numbers from your diagnostic report and consider just the first bit of those numbers. Then:
> 
> - Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard numbers which do not match the bit criteria.
> - If you only have one number left, stop; this is the rating value for which you are searching.
> - Otherwise, repeat the process, considering the next bit to the right.

Compared to part one, the main difference is that the most and least common bit must be re-computed with the remaining numbers.

## 🤔🤯 Puzzle Solver

An easy solution is to narrow down on the number matching most bits and least bits in separate loops. 

```python
def solve_part_two(diagnostic_report: Iterator[tuple]) -> int:
    """Solve the first part of the challenge

    :param diagnostic_report: binary numbers
    :return: expected challenge answer
    """
    numbers = set(diagnostic_report)
    for bit_index, _ in enumerate(zip(*numbers)):
        bits = list(zip(*numbers))[bit_index]
        values = Counter(bits).most_common()
        if len(values) == 1:
            break
        most_common =\
            values[0][0] if values[0][1] > values[1][1] else '1'
        numbers = set(number for number in numbers if number[bit_index] == most_common)
    oxygen_generator_rating = int(''.join(numbers.pop()), 2)
    numbers = set(diagnostic_report)
    for bit_index, _ in enumerate(zip(*numbers)):
        bits = list(zip(*numbers))[bit_index]
        values = Counter(bits).most_common()
        if len(values) == 1:
            break
        least_common =\
            values[1][0] if values[0][1] > values[1][1] else '0'
        numbers = set(number for number in numbers if number[bit_index] == least_common)
    co2_scrubber_rating = int(''.join(numbers.pop()), 2)
    answer = oxygen_generator_rating * co2_scrubber_rating
    return answer
```

There is room for improvement has this method could be nearly completely factorized.

Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day_3.py input.txt -p 2` | `1007985` | 36.9 ms

[aoc]: https://adventofcode.com/
[aoc-2021]: https://adventofcode.com/2021/
[aoc-2021-3]: https://adventofcode.com/2021/day/3
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
[py-return]: https://docs.python.org/3/reference/simple_stmts.html#the-return-statement
[py-set]: https://docs.python.org/3/library/stdtypes.html#set
[py-sn]: https://docs.python.org/3/library/types.html#types.SimpleNamespace
[py-split]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.split
[py-string]: https://docs.python.org/3/library/stdtypes.html#textseq
[py-strip]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
[py-sum]: https://docs.python.org/3/library/functions.html#sum
[py-tuple]: https://docs.python.org/3/library/stdtypes.html#tuple
[py-zip]: https://docs.python.org/3/library/functions.html#zip
