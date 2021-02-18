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

Got it.

# 📃➡ Input Contents Format

The input consists in two lines, with each line being a list of tokens separated by a single coma.

Each token being a single character followed by a positive decimal value.
```regexp
[RLUP]\d+
```

# ⚙🚀 Implementation

## 💾🔍 Content Decoding

Input contents are read, transformed and loaded using a dedicated function `load_contents()`.

This function takes a [`str`][py-string] as argument representing the filename containing the contents, and returns two lists of pairs. Each pair is a [`tuple`][py-tuple] representing a single segment of the wire.

```python
def load_contents(filename: str) -> list[list[tuple[int]]]:
    ...
```

The file matching the filename is open; read; and split. The resulting list is then further processed for converting each token into segment offsets.

Token | Segment
--- | ---
`R11` | (11, 0)
`L23` | (-23, 0)
`U27` | (0, 27)
`D31` | (0, -31)

The logic being the following:

* If direction is `L` or `D` then invert the sign
* If direction is `R` or `L` then assign length to first member of the tuple, else assign to the second.

```python
if direction in ['L', 'D']:
    length *= -1
if direction in ['R', 'L']:
    segment = (length, 0)
else:
    segment = (0, length)
    

```

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-2019-3]: https://adventofcode.com/2019/day/3

[py]: https://docs.python.org/3/
[py-string]: https://docs.python.org/3/library/stdtypes.html#textseq
[py-tuple]: https://docs.python.org/3/library/stdtypes.html#tuple

[w-taxicab-geometry]: https://en.wikipedia.org/wiki/Taxicab_geometry
