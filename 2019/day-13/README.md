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

> The game didn't run because you didn't put in any quarters. Unfortunately, you did not bring any quarters. Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free.

The express `memory address 0` likely refers to the following feature detailled in [day 9][aoc-2019-9]:

> Memory beyond the initial program starts with the value `0` and can be read or written like any other memory.

This means that software must be altered prior to running *part two*. The operation would consist in appending the value `0` to the first integer ~~beyond the intial program~~ (turns out that `memory address 0` should be taken literally).

```python
contents.append(0)
```

> The arcade cabinet has a joystick that can move left and right. The software reads the position of the joystick with input instructions:
> ```
> If the joystick is in the neutral position, provide 0.
> If the joystick is tilted to the left, provide -1.
> If the joystick is tilted to the right, provide 1.
> ```

With three choices exploring each round increases by three-fold the number of moves which must be explored.

> The arcade cabinet also has a segment display capable of showing a single number that represents the player's current score. When three output instructions specify `X=-1, Y=0`, the third output instruction is not a tile; the value instead specifies the new score to show in the segment display. For example, a sequence of output values like `-1,0,12345` would show `12345` as the player's current score.

A *simple* change to the `solve` method from part one should do the trick. 

> Beat the game by breaking all the blocks. What is your score after the last block is broken?

Thinking that having a picture representation of the scene may help, something transforming the output list into a dict of x, y tiles.

```
########################################
#                                      #
#   x  xxxx x  x  xxxx     x x xxx x   #
# xxx xx  x xxxxxx  xx   xx  xx xxxx x #
#  xx xxxx xxxx x xx  xxx xxxxxx  xx   #
# xxxx xxxx xxxx xx   x     x  xx x  x #
# xxxxx x x x xxxx x xxx xxxxxx xxx x  #
#  x xxxx x  x xx     xxx  x xx xx     #
#  x  xxxxxxxxxxx x  xxxxx xxx  x   x  #
#  xx x xxx     xxxxxxx  x  x xxxxx xx #
#  xxxx x   xxx x x      xx xx  xxxxxx #
#   x x  x x x  x xx  x       xx xxxx  #
#  xxx x x xxxxxxxxxx x   x x x xxxxxx #
# x x xx  xxxxxxx xx   xx xx  x xxxx   #
#  x  xx       x     x xxx  x xx xxxxx #
# x  x  xxx   xxxxxxx xxxxxx  xx x  xx #
# xx  xxxx xxxx    x xxx x   x x    x  #
# xx xxx xxxxxxxxxxxxx        x xxxx x #
#                                      #
#                 o                    #
#                                      #
#                                      #
#                   =                  #
#                                      #
```

Turns out that the arcade wasn't a flipper but a pong! This explains a lot of things and greatly simplifies the logic for governing the joystick as we only want to track the vertical position of the ball!

## 🤔🤯 Puzzle Solver

First thing is to get the game running by applying the indicated change.

```python
contents[0] = 2
```

Next thing is to provide joystick inputs. Providing a single joystick input triggers an internal error:

```
IndexError: pop from empty list
```

This error provides insights on how the program behaves:

* a `halt` instruction is triggered when the game is over
* joystick commands are popped during game execution

Rather than breaking on `halt` instructions, breaking on outputs which update the ball position may be much better as we could deduce the correct joystick input.


For the game to continue, the paddle must track the ball hence the need for a method returning the position of the ball or the paddle on the horizontal axis.

```python
def get_position(tiles: list, tile_type: TilesTypes) -> any:
    filtered_tiles = [t[0:2] for t in tiles if t[2] == tile_type]
    if not len(filtered_tiles):
        return None
    return filtered_tiles[-1][0]
```

For each ball position update, its next position must get computed:

```python
next_ball_position = ball_position + (ball_position - last_ball_position)
```

This value is then compared with the position of the paddle for determining the next action:

```python
if next_ball_position < paddle_position:
    inputs.append(Joystick.LEFT)
elif next_ball_position == paddle_position:
    inputs.append(Joystick.NEUTRAL)
elif next_ball_position > paddle_position:
    inputs.append(Joystick.RIGHT)
```

The exit condition being an `halt` instruction, after which the expected solution value is computed:

```python
    block_tiles = Counter(tile_ids)[TilesTypes.BLOCK]
    if block_tiles == 0:
        return map_[(-1, 0)]
```

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-13.py input.txt -p 2` | `15706`

# 🚀✨ Further Improvements

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-9]: https://adventofcode.com/2019/day/9
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
