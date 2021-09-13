Solution in [Python][py] for the [day 15 puzzle][aoc-2019-15] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Oxygen System 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> Out here in deep space, many things can go wrong. Fortunately, many of those things have indicator lights. Unfortunately, one of those lights is lit: the oxygen system for part of the ship has failed!

Believe I saw this in a movie.

> According to the readouts, the oxygen system must have failed days ago after a rupture in oxygen tank two; that section of the ship was automatically sealed once oxygen levels went dangerously low. A single remotely-operated repair droid is your only option for fixing the oxygen system.

On the other hand I don't remember of any droid.

> The Elves' care package included an Intcode program (your puzzle input) that you can use to remotely control the repair droid. By running that program, you can direct the repair droid to the oxygen system and fix the problem.

*Intcode* it is then!

> The remote control program executes the following steps in a loop forever:
> 
> Accept a movement command via an input instruction.

At least the usage of an input instruction is spelled out.

> Send the movement command to the repair droid.
> Wait for the repair droid to finish the movement operation.
> Report on the status of the repair droid via an output instruction.
>
> Only four movement commands are understood: north (1), south (2), west (3), and east (4). Any other command is invalid. The movements differ in direction, but not in distance: in a long enough east-west hallway, a series of commands like 4,4,4,4,3,3,3,3 would leave the repair droid back where it started.

This allows us to lay out the first constant data structure.

Value | Description
--- | ---
1 | Move north
2 | Move south
3 | Move west
4 | Move east

```python
class Movement(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
```

> The repair droid can reply with any of the following status codes:
> 
> * 0: The repair droid hit a wall. Its position has not changed.
> * 1: The repair droid has moved one step in the requested direction.
> * 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.

Here goes the second constant data structure.

Value | State | Position | On oxygen
--- | --- | --- | ---
0 | Hit a wall | Unchanged | False
1 | Moved a single step | Changed | False
2 | Moved a single step | Changed | True

```python
class StatusCodes(IntEnum):
    BLOCKED = 0
    MOVED_NO_OXYGEN = 1
    MOVED_GOT_OXYGEN = 2

status = {
    StatusCodes.BLOCKED: {
        'update_position': False,
        'on_oxygen': False
    },
    StatusCodes.MOVED_NO_OXYGEN: {
        'update_position': True,
        'on_oxygen': False
    },
    StatusCodes.MOVED_GOT_OXYGEN: {
        'update_position': True,
        'on_oxygen': True
    },
}
```

> 
> You don't know anything about the area around the repair droid, but you can figure it out by watching the status codes.
> 
> For example, we can draw the area using `D` for the droid, `#` for walls, `.` for locations the droid can traverse, and empty space for unexplored locations. Then, the initial state looks like this:
> 
> 
> ```
> D  
> ```
> 
> 
> To make the droid go north, send it 1. If it replies with 0, you know that location is a wall and that the droid didn't move:
> 
> ```
> #  
> D  
> ```
> 
> 
> To move east, send 4; a reply of 1 means the movement was successful:
> 
> ```
> #  
> .D 
> ```
> 
> 
> Then, perhaps attempts to move north (1), south (2), and east (4) are all met with replies of 0:
> 
> ```
> ## 
> .D#
> # 
> ```
> 
> Now, you know the repair droid is in a dead end. Backtrack with 3 (which you already know will get a reply of 1 because you already know that location is open):
> 
> ```
> ## 
> D.#
> # 
> ```
> 
> Then, perhaps west (3) gets a reply of 0, south (2) gets a reply of 1, south again (2) gets a reply of 0, and then west (3) gets a reply of 2:
> 
> ```
> ## 
> #..#
> D.# 
> #  
> ```
> Now, because of the reply of 2, you know you've found the oxygen system! In this example, it was only 2 moves away from the repair droid's starting position.
> 
> What is the fewest number of movement commands required to move the repair droid from its starting position to the location of the oxygen system?

## 💾🔍 Content Decoding

Since this puzzle deals with Intcode, content decoding methods can be reused.

```python
def load_contents(filename: Path) -> Iterator[map]:
    """Load and convert contents from file

    :param filename: input filename
    :return: iterator yielding a map of the address and its intcode
    """
    lines = iter(open(filename).read().strip().split(os.linesep))
    for line in lines:
        yield {i: int(token) for i, token in enumerate(line.split(','))}
    log.debug(f'Reached end of {filename=}')
```

A small improvement is the use of an iterator with the `iter()` keyword, which avoids having to reconstruct the complete list before iterating over it.

## 💡🙋 Implementation

Looking at the Intcode program, the first instruction is `3` which reads an input value and stores it on the pointer located in the following integer `1033`. This means that an input must be provided from the start.

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-2019-15]: https://adventofcode.com/2019/day/15
[py]: https://docs.python.org/3/
