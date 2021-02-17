Solution in [Python][py] for the [day 2 puzzle][aoc-2019-2] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 1202 Program Alarm 🎄🌟🌟

* Part one: [statement](#-puzzle-statement-with-annotations) / [implementation](#-implementation)
* Part two: [statement](#-annotated-description) / [implementation](#-solver-implementation)

# 🔍📖 Puzzle Statement with Annotations

Would this puzzle relate to the infamous [error code][w-1202] during the [Apollo 11 lunar descent][w-descent]?

> On the way to your gravity assist around the Moon, your ship computer beeps angrily about a "1202 program alarm". On the radio, an Elf is already explaining how to handle the situation: "Don't worry, that's perfectly norma--" The ship computer bursts into flames.

These Elves are quite the bunch.

> You notify the Elves that the computer's magic smoke seems to have escaped. "That computer ran Intcode programs like the gravity assist program it was working on; surely there are enough spare parts up there to build a new Intcode computer!"

Seems that this puzzle involves creating a --brace for it-- virtual machine for emulating the *Intcode* computer! 

> An Intcode program is a list of integers separated by commas (like 1,0,0,3,99). To run one, start by looking at the first integer (called position 0). Here, you will find an opcode - either 1, 2, or 99. The opcode indicates what to do; for example, 99 means that the program is finished and should immediately halt. Encountering an unknown opcode means something went wrong.

Three opcodes --may be more for part two?--.

* `99`: halt
* `1` or `2`: some sort of instruction
* other: implementation issue

> Opcode `1` adds together numbers read from two positions and stores the result in a third position. The three integers immediately after the opcode tell you these three positions - the first two indicate the positions from which you should read the input values, and the third indicates the position at which the output should be stored.

This instruction uses pointers as arguments. These pointers are relative to the first item in the program, which should be a valid instruction.

> For example, if your Intcode computer encounters 1,10,20,30, it should read the values at positions 10 and 20, add those values, and then overwrite the value at position 30 with their sum.

Example checks out.

> Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them. Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.

Sounds legit.

> Once you're done processing an opcode, move to the next one by stepping forward 4 positions.

All right.

> For example, suppose you have the following program:
> 
> 1,9,10,3,2,3,11,0,99,30,40,50
> 
> For the purposes of illustration, here is the same program split into multiple lines:
> 
> ```
> 1,9,10,3,
> 2,3,11,0,
> 99,
>  30,40,50
> ```

It should be expected that the program is able to modify data which is located ahead of the [program counter][w-pc]. 

> The first four integers, 1,9,10,3, are at positions 0, 1, 2, and 3. Together, they represent the first opcode (1, addition), the positions of the two inputs (9 and 10), and the position of the output (3). To handle this opcode, you first need to get the values at the input positions: position 9 contains 30, and position 10 contains 40. Add these numbers together to get 70. Then, store this value at the output position; here, the output position (3) is at position 3, so it overwrites itself. Afterward, the program looks like this:
> 
> ```
> 1,9,10,70,
> 2,3,11,0,
> 99,
> 30,40,50
> ```
> 
> Step forward 4 positions to reach the next opcode, 2. This opcode works just like the previous, but it multiplies instead of adding. The inputs are at positions 3 and 11; these positions contain 70 and 50 respectively. Multiplying these produces 3500; this is stored at position 0:
> 
> ```
> 3500,9,10,70,
> 2,3,11,0,
> 99,
> 30,40,50
> ```

Got it.

> Stepping forward 4 more positions arrives at opcode 99, halting the program.
> 
> Here are the initial and final states of a few more small programs:
> 
> ```
> 1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
> 2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
> 2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
> 1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.
> ```

Makes sense.

> Once you have a working computer, the first step is to restore the gravity assist program (your puzzle input) to the "1202 program alarm" state it had just before the last computer caught fire.
> 
> To do this, before running the program, replace position 1 with the value 12 and replace position 2 with the value 2. What value is left at position 0 after the program halts?

After loading contents, the following changes must be applied:

1. Set value `12` at position `1`.
1. Set value `2` at position `2`.

To be honest these changes are perplexing: why aren't they already incorporated in the input contents to start with? The answer probably has to do with part two.

# 📃➡ Input Contents Format

Input contents are retrieved through a separate file. They are encoded as a series of integers separated by a single comma character.

For instance, the example program is:
```
1,9,10,3,2,3,11,0,99,30,40,50
```

# ⚙🚀 Implementation

## 💾🔍 Content Decoding

Input content decoding is managed by a dedicated function `load_contents()`, which receives a filename as an input argument and returns a list of integers.

```python
def load_contents(filename: str) -> list[int]:
    ...
```

The file contents are read and cleansed using standard Python methods [`open()`][py-open], [`read()`][py-read], [`strip()`][py-strip] and [`split()`][py-split].

The list of strings is converted to a list of integers using [`map()`][py-map].

```python
def load_contents(filename: Path) -> list[int]:
    contents = list(map(int, open(filename).read().strip().split(',')))
    return contents
```

## 💡🙋 Puzzle Solving

The last paragraph of the puzzle statement requests the contents to be altered.

> The first step is to restore the gravity assist program (your puzzle input).

The changes consist in writing `1202` as two values `12` and `02` in the instructions located position 1 and 2.

```python
def patch(program: list[int]) -> list[int]:
    program[1] = 12
    program[2] = 2
    return program
```

The program counter then requires to be set to zero, and the processing loop entered. It will be exited when executing the `halt` instruction.

```python
input_program = len(contents) > 12
program = patch(program=contents) if input_program else contents
pc = 0
instr = program[pc]
while instr in [ADD, MUL]:
    a_ptr, b_ptr, r_ptr = program[pc + 1:pc + 4]
    a, b = [program[ptr] for ptr in [a_ptr, b_ptr]]
    program[r_ptr] = execute(instruction=instr, operand_a=program[a_ptr],
                             operand_b=program[b_ptr])
    pc += 4
    instr = program[pc]
```

With the execute() method simply decoding the instruction:

```python
def execute(instruction: int, operand_a: int, operand_b: int) -> int:
    if instruction == ADD:
        return operand_a + operand_b
    if instruction == MUL:
        return operand_a * operand_b
```

> What value is left at position 0 after the program halts?

The answer is obtained by reading the first item of the program.

```python
answer = program[0]
return answer
```

Contents | Answer
--- | ---
[`example.txt`](./example.txt) | `3500`
[`input.txt`](./input.txt) | `3166704`

# 😰🙅 Part Two

## 🥺👉👈 Annotated Description

> "Good, the new computer seems to be working correctly! Keep it nearby during this mission - you'll probably use it again. Real Intcode computers support many more features than your new one, but we'll let you know what they are as you need them."

*Probably use it again*?! better be so!

> "However, your current priority should be to complete your gravity assist around the Moon. For this mission to succeed, we should settle on some terminology for the parts you've already built."
> 
> Intcode programs are given as a list of integers; these values are used as the initial state for the computer's memory. When you run an Intcode program, make sure to start by initializing memory to the program's values. A position in memory is called an address (for example, the first value in memory is at "address 0").
> 
> Opcodes (like 1, 2, or 99) mark the beginning of an instruction. The values used immediately after an opcode, if any, are called the instruction's parameters. For example, in the instruction 1,2,3,4, 1 is the opcode; 2, 3, and 4 are the parameters. The instruction 99 contains only an opcode and has no parameters.
> 
> The address of the current instruction is called the instruction pointer; it starts at 0. After an instruction finishes, the instruction pointer increases by the number of values in the instruction; until you add more instructions to the computer, this is always 4 (1 opcode + 3 parameters) for the add and multiply instructions. (The halt instruction would increase the instruction pointer by 1, but it halts the program instead.)

Explanations on terminology and concepts.

> "With terminology out of the way, we're ready to proceed. To complete the gravity assist, you need to determine what pair of inputs produces the output 19690720."

The **pair of inputs** most likely refers to the two integers changed prior executing the Intcode program.

> The inputs should still be provided to the program by replacing the values at addresses 1 and 2, just like before. In this program, the value placed in address 1 is called the noun, and the value placed in address 2 is called the verb. Each of the two input values will be between 0 and 99, inclusive.

Each item taking 100 different values yields *10,000* possible combinations.

> Once the program has halted, its output is available at address 0, also just like before. Each time you try a pair of inputs, make sure you first reset the computer's memory to the values in the program (your puzzle input) - in other words, don't reuse memory from a previous attempt.

Obviously contents of the Intcode program are subject to change. However since the instructions take the values `1` and `2` it is likely that they are not modified during the execution of the program. This would allow to factorize the operations for computing the value at position zero. All this could be premature optimization though if the initial brute force approach yields a result in a reasonable time.

> Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)

The computation of the answer as described here is not compatible with one from part one.

## 🤔🤯 Solver Implementation

Whereas in part one the noun and verb were respectively `12` and `2`, in this part they must both be cycled through between `0` and `99`. This requires modifying the `patch()` method from part one by exposing the arguments `noun` and `verb`.

```python
def patch(program: list[int], noun: int, verb: int) -> list[int]:
    program[1] = noun
    program[2] = verb
    return program
```

Lastly a `solve_part_two()` method must be implemented. In the first implementation it consists of the `solve()` body with a outer loop for cycling through all values on the `noun` and `verb` variables.

```python
REQUESTED_OUTPUT = 19690720
...
input_program = len(contents) > 12
upper_bound = 100 if input_program else len(contents)
for noun in range(upper_bound):
    for verb in range(upper_bound):
        first_position = execute_program(
            contents=contents.copy(), noun=noun, verb=verb)
        if REQUESTED_OUTPUT == first_position:
            ...
```

The computation of the answer remains straight forward.

```python
answer = 100 * noun + verb
return answer
```

Contents | Answer
--- | ---
[`example.txt`](./example.txt) | **None**
[`input.txt`](./input.txt) | `8018`

No pairs of `noun` and `verb` values yield the required `19690720` value when run on the Intcode program loaded from [`example.txt`](./example.txt).

# 🙄😔 Closing Thoughts

The part two of this puzzle was solved with a brute force approach. It would have been much more complex with greater bounds for the *noun* and *verb* variables, were some sort of unrolling and graph traversal being required. They will likely be the topics of the following puzzles!

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-2019-2]: https://adventofcode.com/2019/day/2

[py]: https://docs.python.org/3/
[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-exit]: https://docs.python.org/3/library/sys.html?highlight=sys%20exit#sys.exit
[py-list]: https://docs.python.org/3/library/functions.html#func-list
[py-main]: https://docs.python.org/3/library/__main__.html
[py-map]: https://docs.python.org/3/library/functions.html#map
[py-name]: https://docs.python.org/3/library/stdtypes.html#definition.__name__
[py-open]: https://docs.python.org/3/library/functions.html#open
[py-read]: https://docs.python.org/3/library/io.html#io.TextIOBase.read
[py-split]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.split
[py-strip]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
[py-sum]: https://docs.python.org/3/library/functions.html#sum

[w-map-reduce]: https://en.wikipedia.org/wiki/MapReduce
[w-advent-calendar]: https://en.wikipedia.org/wiki/Advent_calendar
[w-1202]: https://en.wikipedia.org/wiki/Apollo_Guidance_Computer#1202_program_alarm
[w-descent]: https://en.wikipedia.org/wiki/Apollo_11#Lunar_descent
[w-pc]: https://en.wikipedia.org/wiki/Program_counter
