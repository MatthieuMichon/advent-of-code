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

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-1.py input.txt -p 1` | `1292`

[aoc]: https://adventofcode.com/
[aoc-2021]: https://adventofcode.com/2021/
[aoc-2021-1]: https://adventofcode.com/2021/day/1
[py]: https://docs.python.org/3/
