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

# 📃➡️ Input File Format 📃➡️

```
51590
53619
101381
81994
139683
[...]
```

The personal puzzle input consists in a number of lines, with each line containing one integer encoded as a string. 

## 🔰📃➡ Example File 🔰📃➡

Using the same encoding for the reference contents and the input contents allows using an identical code path for both. The only drawback appears that automating value checking is more complex.

However since the example test set consists of just a few input value and a single result, a manual check is still adequate at this scale.

```
12
14
1969
100756
```


[py]: https://docs.python.org/3/
[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-2019-1]: https://adventofcode.com/2019/day/1
[reddit-2019-1]: https://www.reddit.com/e4axxe
[advent-calendar]: https://en.wikipedia.org/wiki/Advent_calendar
[rocket-equation]: https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation
