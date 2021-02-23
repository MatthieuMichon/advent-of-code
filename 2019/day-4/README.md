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

```shell
$ ./day-4.py 168630-718098
```

# ⚙🚀 Implementation

## 💾🔍 Content Decoding

The solving method is likely to process the numbers by doing a per-digit processing, meaning that a list of digits is expected to be more convenient than a simple integer containing all the digits.

```python
def decode(argument: str) -> tuple[list[int], ...]:
    char_lists = map(list, argument.split('-'))
    range_ = tuple(list(map(int, clist)) for clist in char_lists)
    return range_
```

> 📝 **Note**
> 
> This method could be avoided by hard-coding the input `168630-718098` directly into the `solve()` method. However, this would be no fun and sometimes I an in the mood of taking the long way home.

## 💡🙋 Puzzle Solving

For the fun lets use a depth-first recursion. The goal is to repeat the following operations:
1. Test if the two last digits are in descending order (i.e `digits[-1] < digits[-2]`), if `True` return zero.
1. Test if all digits are present, if `True` then
    1. Test if two or more adjacent digits are the same (see note below), if `True` return `1` since the corresponding password is valid. Oppositely return zero.
1. Not all digits are present, we compute lower and upper ranges.
1. Loop over all ten digits
    1. Append this digit to the digits computed in parent.
    1. Expedite iteration (i.e `continue` iterating) if the obtained value is out of the range.
    1. If the obtained is in range than call recursively the function, accumulate the result.
1. Return the accumulated value.
       
> 📝 **Note**
> 
> Since digits are equal or increasing the further to the right, if two digits are identical they must be adjacent, thus this test is implemented simply by comparing lengths of the [`list`][py-list] against length of the [`set`][py-set].

```python
def count_pwd(range_: tuple[list[int], ...],
              digits: list[int], length: int) -> int:
    digit_index = len(digits)
    decreasing_digit = digit_index >= 2 and digits[-1] < digits[-2]
    if decreasing_digit:
        return 0
    stop = digit_index == length
    if stop:
        same_adjacent_digits = len(set(digits)) < len(digits)
        return 1 if same_adjacent_digits else 0
    min_digits = range_[0][:1+digit_index]
    max_digits = range_[1][:1+digit_index]
    pwd_count = 0
    for next_digit in range(10):
        next_digits = digits.copy()
        next_digits.append(next_digit)
        if not min_digits <= next_digits <= max_digits:
            continue
        pwd_count += count_pwd(
            range_=range_, digits=next_digits, length=length)
    return pwd_count
```

Contents | Answer
--- | ---
`168630-718098` | `1686`


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
[py-set]: https://docs.python.org/3/library/stdtypes.html#set
[py-split]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.split
[py-string]: https://docs.python.org/3/library/stdtypes.html#textseq
[py-strip]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
[py-sum]: https://docs.python.org/3/library/functions.html#sum
[py-tuple]: https://docs.python.org/3/library/stdtypes.html#tuple

[w-comma]: https://en.wikipedia.org/wiki/Comma#Computing
[w-newline]: https://en.wikipedia.org/wiki/Newline
[w-taxicab-geometry]: https://en.wikipedia.org/wiki/Taxicab_geometry
[w-distance]: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
