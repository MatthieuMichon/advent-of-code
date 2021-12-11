Solution in [Python][py] for the [day 1 puzzle][aoc-2021-1] of the [2021 edition][aoc-2021] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Sonar Sweep 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> On a small screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the sea floor depth as the sweep looks further and further away from the submarine.
>
> The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.
> 
> To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:
> 
> ```
> 199 (N/A - no previous measurement)
> 200 (increased)
> 208 (increased)
> 210 (increased)
> 200 (decreased)
> 207 (increased)
> 240 (increased)
> 269 (increased)
> 260 (decreased)
> 263 (increased)
> ```
> 
> In this example, there are `7` measurements that are larger than the previous measurement.

How many measurements are larger than the previous measurement?

## 💾🔍 Content Decoding

Each line contains just one integer, making the parsing easy.

```python
def load_contents(filename: Path) -> Iterator[int]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding integers
    """
    lines = iter(open(filename).read().strip().split(os.linesep))
    for line in lines:
        yield int(line)
    log.debug(f'Reached end of {filename=}')
```

## 💡🙋 Implementation

The solver for this first challenge consists in a simple loop using `enumerate()` as to provide an index for checking the edge case of the first index.

```python
def solve_part_one(depths: [int]) -> int:
    """Solve the first part of the challenge

    :param depths: list of depth values
    :return: expected challenge answer
    """
    answer = 0
    for i, depth in enumerate(depths):
        first_depth = i == 0
        prev_depth = depths[0] if first_depth else depths[i-1]
        answer += 1 if depth > prev_depth else 0
    return answer
```

Looking back at the code, one can't help but think that _there must be a better way_ to run this computation, which at its core is a sum of cases satisfying a simple condition, which is no other that the following depth is greater.

First a list must be transformed into a list of consecutive pairs, for example `[1, 2, 3, 4]` should become `[[1, 2], [2, 3], [3, 4]]`. This is most simply done using the [`zip()`][py-zip] method.

```python
int_list = [1, 2, 3, 4]
consecutive_pairs = zip(int_list[:-1], int_list[1:])
print(list(consecutive_pairs))
# [(1, 2), (2, 3), (3, 4)]
```

Thus, the idea would rely on the [`sum()`][py-sum] method applied on a _greater than_ operator. What remains is iterating over the whole list.

```python
consecutive_pairs = zip(int_list[:-1], int_list[1:])
answer = sum(a > b for a, b in consecutive_pairs)
```

At the end the source becomes much cleaner:

```python
def solve_part_one(depths: [int]) -> int:
    """Solve the first part of the challenge

    :param depths: list of depth values
    :return: expected challenge answer
    """
    pairs = zip(depths[:-1], depths[1:])
    answer = sum(a < b for a, b in pairs)
    return answer
```

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-1.py input.txt -p 1` | `1292`

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

> Instead, consider sums of a three-measurement sliding window. Again considering the above example:
> 
> ```
> 199  A      
> 200  A B    
> 208  A B C  
> 210    B C D
> 200  E   C D
> 207  E F   D
> 240  E F G  
> 269    F G H
> 260      G H
> 263        H
> ```
> 
> Start by comparing the first and second three-measurement windows. The measurements in the first window are marked A (199, 200, 208); their sum is 199 + 200 + 208 = 607. The second window is marked B (200, 208, 210); its sum is 618. The sum of measurements in the second window is larger than the sum of the first, so this first comparison increased.

Idea is, instead of processing and slicing the list into a pair of integers, to compute two sets of three integers; do their sum and finally compare them. 

> In the above example, the sum of each three-measurement window is as follows:
> 
> ```
> A: 607 (N/A - no previous sum)
> B: 618 (increased)
> C: 618 (no change)
> D: 617 (decreased)
> E: 647 (increased)
> F: 716 (increased)
> G: 769 (increased)
> H: 792 (increased)
> ```
> 
> Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum?

This second part is not that different from the first one.

## 🤔🤯 Puzzle Solver

The following processing steps are required:

- Convert the list of integers into a list of tuples by producing slices using `zip()` of three integers each one with an offset shifted by one, changing the range boundaries.
- Convert a second time the list with all the range boundaries shifted by one: `depths[1:-2], depths[2:-1], depths[3:]` instead of `depths[:-3], depths[1:-2], depths[2:-1]`.
- For both lists compute the sum for each tuple
- Compare these sums like was done in part one.

```python
def solve_part_two(depths: [int]) -> int:
    """Solve the second part of the challenge

    :param depths: list of depth values
    :return: expected challenge answer
    """
    baseline = zip(depths[:-3], depths[1:-2], depths[2:-1])
    baseline_sums = (sum(i) for i in baseline)
    sample = zip(depths[1:-2], depths[2:-1], depths[3:])
    sample_sums = (sum(i) for i in sample)
    pairs = zip(baseline_sums, sample_sums)
    answer = sum(a < b for a, b in pairs)
    return answer
```

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-1.py input.txt -p 2` | `1262`

[aoc]: https://adventofcode.com/
[aoc-2021]: https://adventofcode.com/2021/
[aoc-2021-1]: https://adventofcode.com/2021/day/1
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
