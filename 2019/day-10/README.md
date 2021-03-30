Solution in [Python][py] for the [day 10 puzzle][aoc-2019-10] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Monitoring Station 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> You fly into the asteroid belt and reach the Ceres monitoring station. The Elves here have an emergency: they're having trouble tracking all of the asteroids and can't be sure they're safe.
> 
> The Elves would like to build a new monitoring station in a nearby area of space; they hand you a map of all of the asteroids in that region (your puzzle input).
> 
> The map indicates whether each position is empty (.) or contains an asteroid (#). The asteroids are much smaller than they appear on the map, and every asteroid is exactly in the center of its marked position. The asteroids can be described with X,Y coordinates where X is the distance from the left edge and Y is the distance from the top edge (so the top-left corner is 0,0 and the position immediately to its right is 1,0).

Origin is top-left corner.

> Your job is to figure out which asteroid would be the best place to build a new monitoring station. A monitoring station can detect any asteroid to which it has direct line of sight - that is, there cannot be another asteroid exactly between them. This line of sight can be at any angle, not just lines aligned to the grid or diagonally. The best location is the asteroid that can detect the largest number of other asteroids.

The `line of sight can be at any angle` makes things much more interesting, which is further confirmed with `not just lines aligned to the grid or diagonally`. This will require some thinking.

> For example, consider the following map:
> 
> ```
> .#..#
> .....
> #####
> ....#
> ...##
> ```
> 
> The best location for a new monitoring station on this map is the highlighted asteroid at 3,4 because it can detect 8 asteroids, more than any other location. (The only asteroid it cannot detect is the one at 1,0; its view of this asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse locations; they can detect 7 or fewer other asteroids. Here is the number of other asteroids a monitoring station on each asteroid could detect:
> 
> ```
> .7..7
> .....
> 67775
> ....7
> ...87
> ```

Example makes sense.

> Here is an asteroid (#) and some examples of the ways its line of sight might be blocked. If there were another asteroid at the location of a capital letter, the locations marked with the corresponding lowercase letter would be blocked and could not be detected:
> 
> ```
> #.........
> ...A......
> ...B..a...
> .EDCG....a
> ..F.c.b...
> .....c....
> ..efd.c.gb
> .......c..
> ....f...c.
> ...e..d..c
> ```

This examples hints at a possible implementation, overlay aliasing positions of an asteroid and mark those as empty. 

> Here are some larger examples:
> 
> *Best is 5,8 with 33 other asteroids detected:*
> 
> ```
> ......#.#.
> #..#.#....
> ..#######.
> .#.#.###..
> .#..#.....
> ..#....#.#
> #..#....#.
> .##.#..###
> ##...#..#.
> .#....####
> ```
> 
> *Best is 1,2 with 35 other asteroids detected:*
> 
> ```
> #.#...#.#.
> .###....#.
> .#....#...
> ##.#.#.#.#
> ....#.#.#.
> .##..###.#
> ..#...##..
> ..##....##
> ......#...
> .####.###.
> ```
> 
> *Best is 6,3 with 41 other asteroids detected:*
> 
> ```
> .#..#..###
> ####.###.#
> ....###.#.
> ..###.##.#
> ##.##.#.#.
> ....###..#
> ..#.#..#.#
> #..#.#.###
> .##...##.#
> .....#.#..
> ```
> 
> *Best is 11,13 with 210 other asteroids detected:*
> 
> ```
> .#..##.###...#######
> ##.############..##.
> .#.######.########.#
> .###.#######.####.#.
> #####.##.#.##.###.##
> ..#####..#.#########
> ####################
> #.####....###.#.#.##
> ##.#################
> #####.##.###..####..
> ..######..##.#######
> ####.##.####...##..#
> .#####..#.######.###
> ##...#.##########...
> #.##########.#######
> .####.#.###.###.#.##
> ....##.##.###..#####
> .#.#.###########.###
> #.#.#.#####.####.###
> ###.##.####.##.#..##
> ```
> 
> Find the best location for a new monitoring station. How many other asteroids can be detected from that location?

Puzzle answer is as shown in the previous examples.

## 💾🔍 Content Decoding

We start with these simple requirements:

* Storing all the examples in a single file will prove much more practical than having a single file for each example.
* Each row is a list of binary values: `#` or `.`.
* Each position must be addressed directly with a simple way of computing coordinates.

> :warning: **Warning**:
> 
> Following part using `dict` objects was replaced with a more efficient implementation relying on `sets`.
> This part is kept as reference.

The last arguments strongly makes the case of relying on a [`dict`][py-dict] object for storing an asteroid at a given location defined by a [`tuple`][py-tuple].

```python
>>> asteroids = {(8, 4): True}
>>> asteroids.get((8, 4), False)
True
>>> asteroids.get((8, 5), False)
False
```

Converting cells into items stored into `dict` items is also straight-forward.

```python
asteroids = dict()
for row in lines:
    if len(row) > (os.linesep()):
        for cell in row:
            asteroid = cell == '#'
            if asteroid:
                asteroids[(cell, row)] = True
    else:
        yield asteroids.copy()
        asteroids = dict()
```

This leaves us with the following `load_contents()` method.

```python
def load_contents(filename: str) -> Iterator[map]:
    lines = open(filename).read().strip().split(os.linesep)
    map_ = dict()
    x: int = 0
    for line in lines:
        if len(line):
            for y, char in enumerate(line):
                if char == '.':
                    continue
                position = (x, y)
                map_[position] = char
            x += 1
        else:
            yield map_
            map_ = dict()
            x = 0
```

> :memo: **Note**:
> 
> Following is a better implementation making use of [`sets`][py-set].

```python
def load_contents(filename: str) -> Iterator[set]:
    lines = open(filename).read().strip().split(os.linesep)
    positions = set()
    x = 0
    for line in lines:
        if not len(line):
            yield positions
            positions = set()
            x = 0
            continue
        positions.update({(x, y) for y, c in enumerate(line) if c == '#'})
        x += 1
```

## 💡🙋 Puzzle Solver

First thing is:

* iterate for each asteroid, 
    * list remaining asteroids
    * iterate for each remaining asteroid
        * compute its positional offset with regard to the reference asteroid

```python
for asteroid in contents:
    others = contents - {asteroid}
    others = {tuple(a - b for a, b in zip(asteroid, o)) for o in others}
```

Contents | Answer
--- | ---

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

## 🤔🤯 Puzzle Solver

Contents | Answer
--- | ---

# 🚀✨ Further Improvements

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-10]: https://adventofcode.com/2019/day/10

[json]: https://www.json.org/json-en.html

[py]: https://docs.python.org/3/
[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-copy]: https://docs.python.org/3/library/copy.html
[py-counter]: https://docs.python.org/3/library/collections.html#collections.Counter
[py-dict]: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
[py-exit]: https://docs.python.org/3/library/sys.html?highlight=sys%20exit#sys.exit
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

[w-isa]: https://en.wikipedia.org/wiki/Instruction_set_architecture
