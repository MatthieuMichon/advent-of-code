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

According to this statement, this first part is quite straightforward.

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

```python
def solve_part_one(commands: Iterator[tuple]) -> int:
    """Solve the first part of the challenge

    :param commands: list of commands
    :return: expected challenge answer
    """
    forward_pos = 0
    depth = 0
    for command in commands:
        if command[0] == 'forward':
            forward_pos += command[1]
        elif command[0] == 'down':
            depth += command[1]
        elif command[0] == 'up':
            depth -= command[1]
    answer = forward_pos * depth
    return answer
```

Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day_2.py input.txt -p 1` | `1480518` | 11.2 ms

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

> In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different from you first thought:
>
> ```
>    down X increases your aim by X units.
>    up X decreases your aim by X units.
>    forward X does two things:
>        It increases your horizontal position by X units.
>        It increases your depth by your aim multiplied by X.
> ```

Suspiciously easy for a part two!

> Again note that since you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in the positive direction.

> Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?

Same method for computing the answer as in part one.

## 🤔🤯 Puzzle Solver

```python
def solve_part_two(commands: Iterator[tuple]) -> int:
    """Solve the second part of the challenge

    :param commands: list of commands
    :return: expected challenge answer
    """
    forward_pos = 0
    depth = 0
    aim = 0
    for command in commands:
        if command[0] == 'forward':
            forward_pos += command[1]
            depth += aim * command[1]
        elif command[0] == 'down':
            aim += command[1]
        elif command[0] == 'up':
            aim -= command[1]
    answer = forward_pos * depth
    return answer
```

Contents | Command | Answer | Time
--- | --- | --- | ---
[`input.txt`](./input.txt) | `./day_2.py input.txt -p 2` | `1282809906` | 22.5 ms

[aoc]: https://adventofcode.com/
[aoc-2021]: https://adventofcode.com/2021/
[aoc-2021-2]: https://adventofcode.com/2021/day/2
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
