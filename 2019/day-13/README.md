Solution in [Python][py] for the [day 13 puzzle][aoc-2019-13] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Care Package 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> As you ponder the solitude of space and the ever-increasing three-hour roundtrip for messages between you and Earth, you notice that the Space Mail Indicator Light is blinking. To help keep you sane, the Elves have sent you a care package.
> 
> It's a new game for the ship's arcade cabinet! Unfortunately, the arcade is all the way on the other end of the ship. Surely, it won't be hard to build your own - the care package even comes with schematics.
> 
> The arcade cabinet runs Intcode software like the game the Elves sent (your puzzle input).

Great to see we can make good usage of out refactored Intcode methods!

> It has a primitive screen capable of drawing square tiles on a grid. The software draws tiles to the screen with output instructions: every three output instructions specify the x position (distance from the left), y position (distance from the top), and tile id.

So we have a number of 3-item lists, comprising the following elements:

Element | Description | Name
--- | --- | ---
X position | distance from the left | `x`
Y position | distance from the top | `y`
Tile Id | Unique tile identifier | `tile`

> The tile id is interpreted as follows:
> 
> * 0 is an empty tile. No game object appears in this tile.
> * 1 is a wall tile. Walls are indestructible barriers.
> * 2 is a block tile. Blocks can be broken by the ball.
> * 3 is a horizontal paddle tile. The paddle is indestructible.
> * 4 is a ball tile. The ball moves diagonally and bounces off objects.

Not sure what a ball, meaning a `tile id` of value `4` is about.

> For example, a sequence of output values like 1,2,3,6,5,4 would draw a horizontal paddle tile (1 tile from the left and 2 tiles from the top) and a ball tile (6 tiles from the left and 5 tiles from the top).

Kind of get it, I guess.

> Start the game. How many block tiles are on the screen when the game exits?

Ok so no real computing yet!

## 💡🙋 Implementation

Since this puzzle relies on Intcode, we can rip off methods from [day 11](/2019/day-11) which has the latest *Intcode* implementation.

The different types of tiles are mapped into an enum:

```python
class TilesTypes(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZONTAL_PADDLE = 3
    BALL = 4
```


## 💡 Solver

The `solve()` method is slightly modified to accommodate the different expected results. The `output_values` is converted into a list of three-item tuples before being mapped using the `Counter` class.

```python
def solve(contents: map) -> int:
    regs = {'pc': 0, 'rb': 0}
    output_values = step(ram=contents, regs=regs, inputs=[])
    assert len(output_values) % 3 == 0
    tiles_count: int = len(output_values) // 3
    tiles = [output_values[3 * i:3 * i + 3] for i in range(tiles_count)]
    tile_ids = [tile[2] for tile in tiles]
    block_tiles = Counter(tile_ids)[TilesTypes.BLOCK]
    return block_tiles
```

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-13.py input.txt -p 1` | `335`

# 😰🙅 Part Two


## 🥺👉👈 Annotated Statement


## 🤔🤯 Puzzle Solver


Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-13.py input.txt -p 2` | `---`

# 🚀✨ Further Improvements


[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-13]: https://adventofcode.com/2019/day/13

[json]: https://www.json.org/json-en.html

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

[w-cartesian]: https://en.wikipedia.org/wiki/Polar_coordinate_system
[w-polar]: https://en.wikipedia.org/wiki/Polar_coordinate_system
