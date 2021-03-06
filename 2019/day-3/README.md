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
def convert_token(token: str) -> tuple[int, int]:
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

The first step is to build a list of segments from each wire. A [generator][py-generator] function goes through all the offset and yields two points corresponding to a given segment extremities. 

```python
def enumerate_segments(wire: list[tuple[int]]) -> Iterator[tuple[tuple[int]]]:
    last_corner = (0, 0)
    for offset in wire:
        corner = tuple(map(operator.add, last_corner, offset))
        yield tuple([last_corner, corner])
```

An intersection involves one horizontal and one vertical segment, the segments from each wire must be separated into two lists depending on their orientation. 

Luckily, each segments is at a right angle meaning they alternate between horizontal and vertical. Knowing this simplifies sorting.

```python
even_segments = [s for i, s in enumerate(segments) if 0 == i % 2]
odd_segments = [s for i, s in enumerate(segments) if 1 == i % 2]
even_are_vertical = even_segments[0][0][0] == even_segments[0][1][0]
horizontal = odd_segments if even_are_vertical else even_segments
vertical = even_segments if even_are_vertical else odd_segments
segments_by_orientation['horizontal'].append(horizontal)
segments_by_orientation['vertical'].append(vertical)
```

Once all the segments for their respective wire are mapped depending on their orientation, finding the intersections is simply a matter of performing a cross match. Thus the group at index `i` is matched with the group of the opposite wire at index `1 - i`.

```python
intersection_distances = []
for i, hgroud in enumerate(segments_by_orientation['horizontal']):
    for sh in hgroud:
        vgroup = segments_by_orientation['vertical'][1 - i]
        for sv in vgroup:
            if intersects([sh, sv]):
                intersection_distances.append(sum(map(abs, intersect_location([sh, sv]))))
```

The `intersect_location()` computes the location where segments intersect:

```python
def intersect_location(segments: tuple[tuple[tuple[int, int]]]) -> tuple[int, int]:
    if segments[0][0][0] == segments[0][1][0]:
        return (segments[0][0][0], segments[1][0][1])
    else:
        return (segments[1][0][0], segments[0][0][1])

```

This leaves computing the answer which is just a matter of find the smallest value.

```python
answer = min(intersection_distances)
return answer
```

Contents | Answer
--- | ---
[`example.txt`](./example.txt) | `6`; `159`; `135`
[`input.txt`](./input.txt) | `2050`


# 😰🙅 Part Two

## 🥺👉👈 Annotated Description

> It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

Shit just got real!

> To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest.

Luckily for us we choose to rely on steps (i.e segments) as the primary type for computing the answer.

> If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.

This will complicate things a tad.

> The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:
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
> In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.
> 
> However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Having the complete list of intersections is required for this problem.

> Here are the best steps for the extra examples from above:
> 
> ```
> R75,D30,R83,U83,L12,D49,R71,U7,L72
> U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
> R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
> U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
> ```
> 
> What is the fewest combined steps the wires must take to reach an intersection?

The computation of the answer as described here is not compatible with one from part one: a new function computing the number of steps from the central port is required.

## 🤔🤯 Solver Implementation

The solver requires cycling through all the intersections. This computation was already implemented as part of the `solve()` method from part one and provides the following elements:

* `segments_by_orientation`
* `intersections`

```python
segments_per_wires = [list(enumerate_segments(wire=w))
                      for w in contents[0:2]]
combined_steps_list = list()
for location, intersect_segments in intersections.items():
    combined_steps = 0
    for segments in segments_per_wires:
        for segment in segments:
            if not crosses(segment=segment, location=location):
                combined_steps += measure_length(segment=segment)
            else:
                combined_steps += measure_distance(
                    segment=segment, location=location)
                break
    combined_steps_list.append(combined_steps)
```

Computing the number of steps on a given wire separating the central port to an intersection requires a `cross()` method determining if a given location is crossed by a segment.

The computation of the answer remains straight forward.

```python
answer = min(combined_steps_list)
return answer
```

Contents | Answer
--- | ---
[`example.txt`](./example.txt) | `30`; `610`; `410`
[`input.txt`](./input.txt) | `21666`

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-3]: https://adventofcode.com/2019/day/3

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
