Solution in [Python][py] for the [day 4 puzzle][aoc-2021-4] of the [2021 edition][aoc-2021] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Giant Squid 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

Only rows and columns must be considered. Following sorting this leaves ten sets of integers per each grid. 

> The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input).

The input contents are a set consisting of a list of integers, followed by a number of 5x5 grids with each cell being an integer.

> For example:
> ```
> 7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
> 
> 22 13 17 11  0
>  8  2 23  4 24
> 21  9 14 16  7
>  6 10  3 18  5
>  1 12 20 15 19
> 
>  3 15  0  2 22
>  9 18 13 17  5
> 19  8  7 25 23
> 20 11 10 24  4
> 14 21 16 12  6
> 
> 14 21 17 24  4
> 10 16 15  9 19
> 18  8 23 26 20
> 22 11 13  6  5
>  2  0 12  3  7
> ```

The input contents decoder is a little more involved than previously. It must return two elements of distinct type.

> The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

The calculation of the sum requires keeping track of uncalled numbers on the grid. Each grid must keep the state of called numbers.

## 💾🔍 Content Decoding

The first part of the contents is a list of integers separated by a comma. Building this list a matter of splitting a string then mapping each member in the appropriate type.

```python
lines = iter(open(filename).readlines())
called_numbers:Iterator[int] = (int(token) for token in next(lines).split(','))
```

The following part consists in iterating over the remaining lines building a list of bingo grids.

```python
for line in lines:
    short_line = len(line) < BINGO_GRID_SIZE
    if short_line:
        continue
    row_numbers = {int(token) for token in line.strip().split()}
    bingo_grid.append(row_numbers)
    grid_complete = len(bingo_grid) == BINGO_GRID_SIZE
    if grid_complete:
        bingo_grids.append(bingo_grid)
        bingo_grid = []
```

The complete `load_contents()` method being:

```python
def load_contents(filename: Path) -> tuple[Iterator, list]:
    """Load and convert contents from file

    :param filename: input filename
    :return: called numbers and bingo grids
    """
    lines = iter(open(filename).readlines())
    called_numbers:Iterator[int] = (
        int(token) for token in next(lines).split(','))
    bingo_grids = []
    bingo_grid = []
    for line in lines:
        short_line = len(line) < BINGO_GRID_SIZE
        if short_line:
            continue
        row_numbers = {int(token) for token in line.strip().split()}
        bingo_grid.append(row_numbers)
        grid_complete = len(bingo_grid) == BINGO_GRID_SIZE
        if grid_complete:
            bingo_grids.append(bingo_grid)
            bingo_grid = []
    log.debug(f'Reached end of {filename=}')
    return called_numbers, bingo_grids
```

## 💡🙋 Implementation

Working from the end, the answer is the product of the called numbered by the sum of all the unmarked numbers.

```python
def solve_part_one(contents: tuple[Iterator, list]) -> int:
    """Solve the first part of the challenge

    :param diagnostic_report: called numbers and bingo grids
    :return: expected challenge answer
    """
    called_numbers, grids = contents
    called_numbers = 0
    unmarked_numbers = {0}
    for called_number in called_numbers:
        ...
    sum_unmarked_numbers = sum(unmarked_numbers)
    answer = called_number * sum_unmarked_numbers
    return answer
```

The inner loop must iterate over all grids. These grids must contain columns and rows which are updated by removing called numbers.

```python
    for called_number in called_numbers:
        for i, grid in enumerate(processed_grids):
            bingo = False
            for j, row in enumerate(grid):
                if called_number not in row:
                    continue
                processed_grids[i][j] = row - {called_number}
                if not processed_grids[i][j]:
                    processed_grids[i].pop(j)
                    bingo = True
            if bingo:
                unmarked_numbers = {n for row in processed_grids[i] for n in row}
                break
        else:
            continue
        break
```


Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day-4.py input.txt -p 1` | `35711` | 62.5 ms

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement


## 🤔🤯 Puzzle Solver

[aoc]: https://adventofcode.com/
[aoc-2021]: https://adventofcode.com/2021/
[aoc-2021-4]: https://adventofcode.com/2021/day/4
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
