Solution in [Python][py] for the [day 2 puzzle][aoc-2021-2] of the [2021 edition][aoc-2021] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Dive! 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:
> 
> - forward X increases the horizontal position by X units.
> - down X increases the depth by X units.
> - up X decreases the depth by X units.
> 
> After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)
> 
> Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?

## 💾🔍 Content Decoding

Opening the input contents file, we notice that each line starts with command followed by a quantity.

First, let's confirm this assumption:

```python
for line in open('./advent-of-code/2021/day-2/input.txt').readlines():
    assert len(line.split()) == 2 \
        and line.split()[0] in ['forward', 'up', 'down'] \
        and line.split()[1].isdigit()
```

Which is does great! We can move and create a proper method this time. Before creating said method, we must agree on a return type. 

Looking at the input contents files, we have a number of lines with no relationship between them. An [iterator](py-iterator) is a good fit for such scenarios promoting sequential processing. This means that the method uses a `yield` statement instead of `return`.

The structure of each line is a string followed by an integer. Thus, the return object is `Iterator[tuple]`

```python
def load_contents(filename: Path) -> Iterator[tuple]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator
    """
    for line in open(filename).readlines():
        items = line.split()
        yield items[0], int(items[1])
    log.debug(f'Reached end of {filename=}')
```

## 💡🙋 Implementation



Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day-2.py input.txt -p 1` | `1480518` | 11.2 ms

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement



## 🤔🤯 Puzzle Solver


Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-2.py input.txt -p 2` | ⏱

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
