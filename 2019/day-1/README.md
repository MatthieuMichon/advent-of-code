Solution in [Python][py] for the [day 1 puzzle][aoc-2019-1] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 The Tyranny of the Rocket Equation 🎄🌟🌟

Chances are this puzzle has something in common with the [equation named after it][rocket-equation].

# 🔍📖 Puzzle Statement with Annotations 🔍📖

> Santa has become stranded at the edge of the Solar System while delivering presents to other planets! To accurately calculate his position in space, safely align his warp drive, and return to Earth in time to save Christmas, he needs you to bring him measurements from fifty stars.
>
> Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Not relevant to the puzzle, presents the premise of the 2019 edition. 

> The Elves quickly load you into a spacecraft and prepare to launch.

Damn elves, always messing things up!!

> At the first Go / No Go poll, every Elf is Go until the Fuel Counter-Upper. They haven't determined the amount of fuel required yet.

*Upper* as in *upper-stage* of a multi-stage rocket? Will keep this in mind for part two maybe.

> Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

Required fuel for a module is the module mass divided by three, rounded down [to the closest integer] and subtracted two.

> For example:
>
> * For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
> * For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
> * For a mass of 1969, the fuel required is 654.
> * For a mass of 100756, the fuel required is 33583.

Math checks out on the two first examples. Two last ones will require spinning up a calculator and they also check out fine.

> The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.

The answer is the total of all the results obtained for each computation.

> What is the sum of the fuel requirements for all of the modules on your spacecraft?

This questions is consistent with the previous statement.

# 📃➡️ Input Contents Format 📃➡️

```
51590
53619
101381
81994
139683
[...]
```

The personal puzzle input consists in a number of lines, with each line containing one integer encoded as a string. 

## 🔰📃➡ Example Contents Format 🔰📃➡

Using the same encoding for the reference contents and the input contents allows using an identical code path for both.

A drawback is that doing so makes automatic testing is more complex.

With just a few input values and a single result, a manual check is just fine, and thus how I go forward.

```
12
14
1969
100756
```

# ➡🙋 Answer Format ➡🙋

The answer is described as a sum, meaning that it can simply be a printout in the console.

# ⚙️🚀 Implementation ⚙🚀

## 🖐️⌨️ Command Line Interface 🖐️🙌️

I chosen to implement all command line interface handling matters in a `main()` method, which receives no arguments and returns an integer used as the exit code passed back to the shell.

```python
#!/usr/bin/env python
import argparse
import sys


EXIT_SUCCESS = 0


def main() -> int:
    args = parse_args()
    contents = load_contents(filename=Path(args.filename))
    answer = solve(contents=contents)
    print(answer)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
``` 

Using stand-alone Python script taking a filename as argument and printing the answer in the terminal allows easy profiling and allows using different contents stored under different filenames without having to edit the script source code.

Industry standard practices call for a [UNIX shebang][shebang] in the first line of the script, and checking [`__name__`][py-name] against [`__main__`][py-main]. Furthermore, proper command line etiquette requires scripts to return `0` for normal behavior and a non-zero value in case of error. In Python the proper way is to rely on [`sys.exit()`][py-exit]. 

Command-line argument management is delegated to the [`argparse`][py-argparse] module, which is provided as a standard Python module since quite a while.

## 🧠🌋 Content Decoding 🧠🌋 

A dedicated `load_contents()` method handles content decoding. Standard Python methods are used.

```python
def load_contents(filename: Path) -> list[int]:
    contents = list(map(int, open(filename).read().strip().split(os.linesep)))
    return contents
```

Starting from the filename argument, the following operations are performed in sequence:

1. a file object is returned by [`open()`][py-open]
1. contents of the file object are serialized using [`read()`][py-read]
1. trailing newlines are removed by calling [`strip()`][py-strip]
1. the string of chars is split into tokens with [`split()`][py-split]
1. per-item type conversion is done through [`map()`][py-map]
1. the generator is iterated using [`list()`][py-list]

## 💡🙋 Puzzle Solving 💡🙋

Solving the first part of the puzzle boils down to performing a [map / reduce][w-map-reduce] operation on the previously loaded contents.

The *map part* consists in applying the calculation listed in the puzzle statement:

> [...] take its mass, divide by three, round down, and subtract 2.

```
fuel = int(mass / 3) - 2
```

Expressed in Python language:

```python
def compute_required_fuel(mass: int) -> int:
    required_fuel = mass // 3 - 2
    return required_fuel
```

The *reduce part* consists in collapsing the list of computed values using the [`sum()`][py-sum] method

```python
answer = sum(required_fuel_values)
```

Computed ansmwers:

* example: `34241`
* input: `3152919`

# 😰🙅 Part Two 😰🙅


[py]: https://docs.python.org/3/
[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-exit]: https://docs.python.org/3/library/sys.html?highlight=sys%20exit#sys.exit
[py-list]: https://docs.python.org/3/library/functions.html#func-list
[py-main]: https://docs.python.org/3/library/__main__.html
[py-map]: https://docs.python.org/3/library/functions.html#map
[py-name]: https://docs.python.org/3/library/stdtypes.html#definition.__name__
[py-open]: https://docs.python.org/3/library/functions.html#open
[py-read]: https://docs.python.org/3/library/io.html#io.TextIOBase.read
[py-split]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.split
[py-strip]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
[py-sum]: https://docs.python.org/3/library/functions.html#sum

[w-map-reduce]: https://en.wikipedia.org/wiki/MapReduce
[shebang]: https://en.wikipedia.org/wiki/Shebang_(Unix)
[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-2019-1]: https://adventofcode.com/2019/day/1
[reddit-2019-1]: https://www.reddit.com/e4axxe
[advent-calendar]: https://en.wikipedia.org/wiki/Advent_calendar
[rocket-equation]: https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation
