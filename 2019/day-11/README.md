Solution in [Python][py] for the [day 11 puzzle][aoc-2019-11] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Space Police 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> On the way to Jupiter, you're pulled over by the Space Police.
> 
> ```
> Attention, unmarked spacecraft! You are in violation of Space Law! 
> All spacecraft must have a clearly visible registration identifier! 
> You have 24 hours to comply or be sent to Space Jail!
> ```
> 
> Not wanting to be sent to Space Jail, you radio back to the Elves on Earth for help. Although it takes almost three hours for their reply signal to reach you, they send instructions for how to power up the emergency hull painting robot and even provide a small Intcode program (your puzzle input) that will cause it to paint your ship appropriately.

Intcode it is! 

> There's just one problem: you don't have an emergency hull painting robot.
> 
> You'll need to build a new emergency hull painting robot. The robot needs to be able to move around on the grid of square panels on the side of your ship, detect the color of its current panel, and paint its current panel black or white. (All of the panels are currently black.)
> 
> The Intcode program will serve as the brain of the robot. The program uses input instructions to access the robot's camera: provide 0 if the robot is over a black panel or 1 if the robot is over a white panel.

Input Value | Panel Color
--- | ---
`0` | Black
`1` | White

> Then, the program will output two values:
> 
> * First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel black, and 1 means to paint the panel white. 
> * Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.

Output Values | Applied Paint | Direction
--- | --- | ---
`0, 0` | Black | Left 90 degrees
`0, 1` | Black | Right 90 degrees
`1, 0` | White | Left 90 degrees
`1, 1` | White | Right 90 degrees

> After the robot turns, it should always move forward exactly one panel. The robot starts facing up.

Initial robot position is `(0, 0)` heading is North.

> The robot will continue running for a while like this and halt when it is finished drawing. Do not restart the Intcode computer inside the robot during this process.
> 
> For example, suppose the robot is about to start running. Drawing black panels as ., white panels as #, and the robot pointing the direction it is facing (< ^ > v), the initial state and region near the robot looks like this:
> 
> ```
> .....
> .....
> ..^..
> .....
> .....
> ```

Memory storage relying on [`dict`][py-dict] are a good fit for situations where there may be an arbitrary number of items and quickly lookup and updates are required.

The robot's heading can be represented by the pointy side as follows:

Heading | Char
--- | ---
North | `^`
East | `>`
South | `v`
West | `<`

> The panel under the robot (not visible here because a ^ is shown instead) is also black, and so any input instructions at this point should be provided 0. Suppose the robot eventually outputs 1 (paint white) and then 0 (turn left). After taking these actions and moving forward one panel, the region now looks like this:
> 
> ```
> .....
> .....
> .<#..
> .....
> .....
> ```
> 
> Input instructions should still be provided 0. Next, the robot might output 0 (paint black) and then 0 (turn left):
> 
> ```
> .....
> .....
> ..#..
> .v...
> .....
> ```
> 
> After more outputs (1,0, 1,0):
> 
> ```
> .....
> .....
> ..^..
> .##..
> .....
> ```
> 
> The robot is now back where it started, but because it is now on a white panel, input instructions should be provided 1. After several more outputs (0,1, 1,0, 1,0), the area looks like this:
> 
> ```
> .....
> ..<#.
> ...#.
> .##..
> .....
> ```

Ok, nothing too fancy.

> Before you deploy the robot, you should probably have an estimate of the area it will cover: specifically, you need to know the number of panels it paints at least once, regardless of color. In the example above, the robot painted 6 panels at least once. (It painted its starting panel twice, but that panel is still only counted once; it also never painted the panel it ended on.)

Ok, so we are going to keep a list of all the panels painted at least once.

> Build a new emergency hull painting robot and run the Intcode program on it. How many panels does it paint at least once?

Sounds fun!

## 💡🙋 Implementation

Looking down from the top-level yields the following tree:

* shell
  * `main()`
    * `load_contents()`
    * `solve()`
      * `step()`
      * `move_robot()`

The main() method remains unchanged from the previous puzzles.

```python
def main() -> int:
    args = parse_arguments()
    configure_logger(verbose=args.verbose)
    compute_part_one = not args.part or 1 == args.part
    compute_part_two = not args.part or 2 == args.part
    if compute_part_one:
        contents = next(load_contents(filename=args.filename))
        answer = solve(contents=contents)
        print(f'part one: {answer=}')
    if compute_part_two:
        answer = -1  # TODO
        print(f'part two: {answer=}')
    return EXIT_SUCCESS
```

### 🔍 Content Decoding

The puzzle input being an *Intcode* program, we can go ahead and shamelessly ripoff the `load_contents()` method of [day-9](/2019/day-9/), with a notable change being that a map with an incremental index is returned instead of a simple list of integers.

```python
def load_contents(filename: str) -> Iterator[map]:
    lines = open(filename).read().strip().split(os.linesep)
    for line in lines:
        yield {i: int(token) for i, token in enumerate(line.split(','))}
```

## 💡 Solver

The `solve()` method is responsible for setting the initial parameters and computing the answer:

```python
def solve(contents: map) -> int:
    robot = {
        'x': 0,
        'y': 0,
        'heading': Directions.NORTH,
        'trail': []
    }
    robot = control_robot(program=contents, initial_state=robot)
    answer = len(set(robot['trail']))
    return answer
```

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-11.py input.txt` | ``

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement


## 🤔🤯 Puzzle Solver


Contents | Answer
--- | ---
[`input.txt`](./input.txt) | ``

# 🚀✨ Further Improvements

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-11]: https://adventofcode.com/2019/day/11

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
