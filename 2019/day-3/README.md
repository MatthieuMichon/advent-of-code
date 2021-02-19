Solution in [Python][py] for the [day 3 puzzle][aoc-2019-3] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Crossed Wires 🎄🌟🌟

# 🔍📖 Annotated Statements

> The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.
> 
> Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).

The puzzle input is described as a list of paths of two wires.

> The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the intersection point closest to the central port. Because the wires are on a grid, use the [Manhattan distance][w-taxicab-geometry] for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.

Ignoring intersections were a wire crossing itself allows searching for said intersections by finding positions which are occupied by more than one wire. This requires beforehand computing the list of locations covered by each wire. 

> For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:
> 
> ```
> ...........
> ...........
> ...........
> ....+----+.
> ....|....|.
> ....|....|.
> ....|....|.
> .........|.
> .o-------+.
> ...........
> ```

The central port would define the location `(0, 0)`.

> Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:
> 
> ```
> ...........
> .+-----+...
> .|.....|...
> .|..+--X-+.
> .|..|..|.|.
> .|.-X--+.|.
> .|..|....|.
> .|.......|.
> .o-------+.
> ...........
> ```
> 
> These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.
> 
> Here are a few more examples:
> 
> ```
> R75,D30,R83,U83,L12,D49,R71,U7,L72
> U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
> R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
> U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
> ```
> What is the Manhattan distance from the central port to the closest intersection?

The answer is based on a unique information, which is located near the start point.

# 📃➡ Input Contents Format

The input consists in two lines, with each line being a list of tokens separated by a single coma.

Each token being a single character followed by a positive decimal value.
```regexp
[RLUP]\d+
```

# ⚙🚀 Implementation

## 💾🔍 Content Decoding

Content decoding tasks are handled in a dedicated [`load_contents()`][py] method.

> 📝 **Note**
> 
> The puzzle description contains a number of examples, with each example being a pair of paths. Storing all of them in a single file (i.e [`examples.txt`](./examples.txt)) allows checking the behavior of the implementation against all of them in a single step (as opposed to having a number of different example files).

This function takes as argument a filename containing the puzzle contents and returns a [`list`][py-list] of pairs of paths. A path consists in a number of offsets encoded as a [`tuple`][py-tuple] of two integers.

```python
def load_contents(filename: str) -> list[list[tuple[int]]]:
    ...
```

The method starts with the usual string of calls: [`open()`][py-open]; [`read()`][py-read]; [`strip()`][py-strip] and [`split()`][py-split] on [newline][w-newline] characters. This provides a list of paths. Each path is a list of segments represented by tokens separated by [comma][w-comma] characters.

> 📝 **Note**
> 
> Segments are encoded in the input contents as a string tokens separated by comas. These tokens start with a single char out of four choices: `R`; `L`; `U` and `D`, followed by a number of digits. Some valid examples being: `D987`; `R18`; `L2` and `U281`.

Conversion of tokens into 2-d grid coordinates is implemented in a [`convert_token()`][src-convert] method.

```python
def convert_token(token: str) -> tuple[int]:
    direction, length = token[:1], int(token[1:])
    assert direction in ['R', 'L', 'U', 'D']
    if direction in ['R', 'U']:
        length *= -1
    offset = (length, 0) if direction in ['R', 'L'] else (0, length)
    return offset
```

The following table contains some examples of conversions.

Token | Offset
--- | ---
`D987` | (0, -987)
`R18` | (18, 0)
`L2` | (-2, 0)
`U281` | (0, 281)

## 💡🙋 Puzzle Solving

Looking at the [`input.txt`](./input.txt) contents shows many segments with three digits values. We can infer that the corresponding grid will be several thousands units wide and tall, meaning that solving by scanning all the locations of the grid is likely to be impractical. 

> 📝 **Note**
> 
> Reviewing the input contents before doing any work on the solver implementation is always a good idea. Doing so provides valuable insights regarding how the size of the dataset, and the space it will occupy during its unfolding.

In fact the wires described in the input contents are extensive.

Spec | First Wire | Second Wire | Code
--- | --- | --- | ---
Segments | 301 | 301 | `[len(w) for w in wires]`
Max length | 995 | 994 | `[max([max(o) for o in w]) for w in wires]`
Average Length | 227 | 253 | `[sum([max(o) for o in w]) // len(w) for w in wires]`

The quantity of segments is low enough to compute the required grid dimensions.

```python
def enumerate_corners(wire: list[tuple[int]]) -> Iterator[tuple[int]]:
    corner = (0, 0)
    for offset in wire:
        corner = tuple(map(operator.add, corner, offset))
        yield corner

>>> min(c[0] for c in corners)
-2909
>>> max(c[0] for c in corners)
4937
>>> min(c[1] for c in corners)
-10352
>>> max(c[1] for c in corners)
1184
```

These values indicate that the minimal 2d grid dimensions are `7846` columns by `11536` rows, amounting to **90 Mcells**. This amount is way too high for any solver relying on scanning individual cells, meaning that the solver should work at the wire segment level to hope achieving an answer fast enough.

> 📝 **Note**
> 
> The magnitude of the grid size dictates the time complexity constraint for solving the puzzle using a reasonable CPU time. The usual limit for Advent of Code being about several seconds as stated in the [Advent of Code introduction][aoc-intro]:
> 
> > [...] every problem has a solution that completes in at most 15 seconds on ten-year-old hardware.

Reading between the lines of the puzzle statement, it is noticed that the answer is computed using a single data point with a localization constraint. This constraint could be used as a criteria for sorting the segments: first segments in the list are the closest from the central point.

A segment consists in the coordinates of its two corners. Its distance with respect to the central point is the diagonal of its fixed axis by its closet point to zero on the variable axis. For example:

* A horizontal segment between `(2, 8)` and `(7, 8)` is `2 + 8`
* A vertical segment between `(-4, 2)` and `(-4, -8)` is `4`

The first step is to compute the list of segments.


[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-3]: https://adventofcode.com/2019/day/3

[py]: https://docs.python.org/3/
[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-exit]: https://docs.python.org/3/library/sys.html?highlight=sys%20exit#sys.exit
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
