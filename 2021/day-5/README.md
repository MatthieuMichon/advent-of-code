Solution in [Python][py] for the [day 5 puzzle][aoc-2021-5] of the [2021 edition][aoc-2021] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Hydrothermal Venture 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:
> 
> ```
> 0,9 -> 5,9
> 8,0 -> 0,8
> 9,4 -> 3,4
> 2,2 -> 2,1
> 7,0 -> 7,4
> 6,4 -> 2,0
> 0,9 -> 2,9
> 3,4 -> 1,4
> 0,0 -> 8,8
> 5,5 -> 8,2
> ```

The input contents are in form of `int,int -> int,int`.

> Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:
>
> - An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
> - An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
> 
> For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

*For now.* guess what is part two.

> So, the horizontal and vertical lines from the above list would produce the following diagram:
> 
> ```
> .......1..
> ..1....1..
> ..1....1..
> .......1..
> .112111211
> ..........
> ..........
> ..........
> ..........
> 222111....
> ```

Such a diagram will also be handy for debug purposes.

> In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or `.` if no line covers that point. The top-left pair of `1`s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.
> 
> To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.
> 
> Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

## 💾🔍 Content Decoding

The input contents are composed of number of independent lines, which was also the case for the prior puzzles of 2021.

```
217,490 -> 217,764
44,270 -> 373,599
440,139 -> 440,303
161,663 -> 345,663
```

The goal is to obtain an efficient structure for storing these data, such as:

```python
((217, 490), (217, 764))
((44, 270), (373, 599))
((440, 139), (440, 303))
((161, 663), (345, 663))
```

Also like for prior puzzles, the contents is handled on a per-line basis using [`readlines()`][py-readlines].

```python
lines = iter(open(filename).readlines())
```

Each single line is composed of the following tokens, separated by a whitespace character.

Position | Type | Regex
--- | --- | ---
#0 | integer | `\d+`
#1 | integer | `\d+`
#2 | string | `->`
#3 | integer | `\d+`
#4 | integer | `\d+`

Parsing these tokens can be done a number of ways:

* regex matching:
  * match the complete line against a regex
  * apply a string to int conversion on all four integers

```python
import re
...
REGEX = r'(\d+),(\d+) -> (\d+),(\d+)'
...
    for line in iter(open(filename).readlines()):
        m = re.search(pattern=REGEX, string=line)
        integers = [int(t) for t in m.groups()]
        yield tuple(integers[0:2]), tuple(integers[2:4])
```

* tokenization:
  * substitute comas by whitespaces
  * split the string between whitespaces
  * discarding the token `->` at position #2 
  * apply a string to int conversion on all four integers

```python
    for line in iter(open(filename).readlines()):
        tokens = line.strip().replace(',', ' ').split(' ')
        tokens.pop(2)
        integers = [int(t) for t in tokens]
        yield tuple(integers[0:2]), tuple(integers[2:4])
```

Comparing the runtime of both implementations, the solution relying on [`split()`][py-split] takes around 30 % less time. The complete method being:

```python
def load_contents_token(filename: Path) -> tuple[tuple, tuple]:
    """Load and convert contents from file

    :param filename: input filename
    :return: coordinates
    """
    for line in iter(open(filename).readlines()):
        tokens = line.strip().replace(',', ' ').split(' ')
        tokens.pop(2)
        integers = [int(t) for t in tokens]
        yield tuple(integers[0:2]), tuple(integers[2:4])
```

## 💡🙋 Implementation

The puzzle states that each set of coordinate represents a vertical or horizontal line. Implementing this processing requires locating the common axis and walking the points between the line ends. 




[aoc]: https://adventofcode.com/
[aoc-2021]: https://adventofcode.com/2021/
[aoc-2021-5]: https://adventofcode.com/2021/day/5
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
[py-readlines]: https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects
[py-return]: https://docs.python.org/3/reference/simple_stmts.html#the-return-statement
[py-set]: https://docs.python.org/3/library/stdtypes.html#set
[py-sn]: https://docs.python.org/3/library/types.html#types.SimpleNamespace
[py-split]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.split
[py-string]: https://docs.python.org/3/library/stdtypes.html#textseq
[py-strip]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
[py-sum]: https://docs.python.org/3/library/functions.html#sum
[py-tuple]: https://docs.python.org/3/library/stdtypes.html#tuple
[py-zip]: https://docs.python.org/3/library/functions.html#zip
