Solution in [Python][py] for the [day 4 puzzle][aoc-2019-4] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Secure Container 🎄🌟🌟

# 🔍📖 Annotated Statements

> You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

No luck!

> However, they do remember a few key facts about the password:
> ```
> It is a six-digit number.
> The value is within the range given in your puzzle input.
> Two adjacent digits are the same (like 22 in 122345).
> Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).                                                                                  
> ```

Six digits numbers can still individually evaluated without requiring too much CPU time.

> Other than the range rule, the following are true:
> ```
> 111111 meets these criteria (double 11, never decreases).
> 223450 does not meet these criteria (decreasing pair of digits 50).
> 123789 does not meet these criteria (no double).
> ```

Understood.

> How many different passwords within the range given in your puzzle input meet these criteria?
> 
> Your puzzle input is 168630-718098.

Iterating it is!

# 📃➡ Input Contents Format

The input is only 13 characters long, meaning that input contents can be passed directly through the command line instead of relying on a file.

# ⚙🚀 Implementation

## 💾🔍 Content Decoding



## 💡🙋 Puzzle Solving


# 😰🙅 Part Two

## 🥺👉👈 Annotated Description




## 🤔🤯 Solver Implementation



[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-4]: https://adventofcode.com/2019/day/4

[py]: https://docs.python.org/3/
[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-exit]: https://docs.python.org/3/library/sys.html?highlight=sys%20exit#sys.exit
[py-generator]: https://docs.python.org/3/library/stdtypes.html#generator-types
[py-list]: https://docs.python.org/3/library/stdtypes.html#list
[py-main]: https://docs.python.org/3/library/__main__.html
[py-map]: https://docs.python.org/3/library/functions.html#map
[py-name]: https://docs.python.org/3/library/stdtypes.html#definition.__name__
[py-open]: https://docs.python.org/3/library/functions.html#open
[py-read]: https://docs.python.org/3/library/io.html#io.TextIOBase.read
[py-split]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.split
[py-string]: https://docs.python.org/3/library/stdtypes.html#textseq
[py-strip]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
[py-sum]: https://docs.python.org/3/library/functions.html#sum
[py-tuple]: https://docs.python.org/3/library/stdtypes.html#tuple

[w-comma]: https://en.wikipedia.org/wiki/Comma#Computing
[w-newline]: https://en.wikipedia.org/wiki/Newline
[w-taxicab-geometry]: https://en.wikipedia.org/wiki/Taxicab_geometry
[w-distance]: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
