Solution in [Python][py] for the [day 5 puzzle][aoc-2019-5] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Sunny with a Chance of Asteroids 🎄🌟🌟

# 🔍📖 Annotated Statements

> You're starting to sweat as the ship makes its way toward Mercury. The Elves suggest that you get the air conditioner working by upgrading your ship computer to support the Thermal Environment Supervision Terminal.

Curious to see how all this pans out. The *TEST* acronym suggests I should be safe with betting on **failure**.

> The Thermal Environment Supervision Terminal (TEST) starts by running a diagnostic program (your puzzle input). The TEST diagnostic program will run on [your existing Intcode computer](../day-2) after a few modifications:

Reads more a day 2 part three.

> First, you'll need to add two new instructions:
> 
> * Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the instruction 3,50 would take an input value and store it at address 50.
> * Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.

Two more instructions with each having only one argument. Curious about how the inputs and outputs are managed.

*Narrator*: they were explained just after.

> Programs that use these instructions will come with documentation that explains what should be connected to the input and output. The program 3,0,4,0,99 outputs whatever it gets as input, then halts.

Previous question is answered.

> Second, you'll need to add support for parameter modes:
> 
> Each parameter of an instruction is handled based on its parameter mode. Right now, your ship computer already understands parameter mode 0, position mode, which causes the parameter to be interpreted as a position - if the parameter is 50, its value is the value stored at address 50 in memory. Until now, all parameters have been in position mode.
> 
> Now, your ship computer will also need to handle parameters in mode 1, immediate mode. In immediate mode, a parameter is interpreted as a value - if the parameter is 50, its value is simply 50.

The two modes being:

* *position mode*, the parameter is a pointer
* *immediate mode*, the parameter is directly the value

> Parameter modes are stored in the same value as the instruction's opcode.

Meaning that the parameter mode can change at each instruction.

> The opcode is a two-digit number based only on the ones and tens digit of the value, that is, the opcode is the rightmost two digits of the first value in an instruction. Parameter modes are single digits, one per parameter, read right-to-left from the opcode:

So the we can split instructions in two parts:

* parameter mode with a width equal in digits to the number of parameters
* 2-digit opcode

> the first parameter's mode is in the hundreds digit, the second parameter's mode is in the thousands digit, the third parameter's mode is in the ten-thousands digit, and so on. Any missing modes are 0.

Agreed.

> For example, consider the program 1002,4,3,4,33.
> 
> The first instruction, 1002,4,3,4, is a multiply instruction - the rightmost two digits of the first value, 02, indicate opcode 2, multiplication. Then, going right to left, the parameter modes are 0 (hundreds digit), 1 (thousands digit), and 0 (ten-thousands digit, not present and therefore zero):
> ```
> ABCDE
>  1002
> 
> DE - two-digit opcode,      02 == opcode 2
>  C - mode of 1st parameter,  0 == position mode
>  B - mode of 2nd parameter,  1 == immediate mode
>  A - mode of 3rd parameter,  0 == position mode,
>                                   omitted due to being a leading zero
> ```

The digit rank of a parameter is `2 + param_number`. Leading zeros are absent, there must be some tricks for handling such case gracefully.

> This instruction multiplies its first two parameters. The first parameter, 4 in position mode, works like it did before - its value is the value stored at address 4 (33). The second parameter, 3 in immediate mode, simply has value 3. The result of this operation, 33 * 3 = 99, is written according to the third parameter, 4 in position mode, which also works like it did before - 99 is written to address 4.

> Parameters that an instruction writes to will never be in immediate mode.

We must still assign outputs using the pointer.

> Finally, some notes:

This can't be good!?

> * It is important to remember that the instruction pointer should increase by the number of values in the instruction after the instruction finishes. Because of the new instructions, this amount is no longer always 4.

This pitfall was identified.

> * Integers can be negative: 1101,100,-1,4,0 is a valid program (find 100 + -1, store the result in position 4).

Didn't saw this one coming.

> The TEST diagnostic program will start by requesting from the user the ID of the system to test by running an input instruction - provide it 1, the ID for the ship's air conditioner unit.

Yes?

> It will then perform a series of diagnostic tests confirming that various parts of the Intcode computer, like parameter modes, function correctly. For each test, it will run an output instruction indicating how far the result of the test was from the expected value, where 0 means the test was successful.

Guess that the outcome will not always be successful.

> Non-zero outputs mean that a function is not working correctly; check the instructions that were run before the output instruction to see which one failed.

Does this means that a correct solver implementation will never output non-zero values? 

> Finally, the program will output a diagnostic code and immediately halt. This final output isn't an error; an output followed immediately by a halt means the program finished. If all outputs were zero except the diagnostic code, the diagnostic program ran successfully.

Ok so all the outputs should be zero.

> After providing 1 to the only input instruction and passing all the tests, what diagnostic code does the program produce?

So all the outputs should be zero except for the last one.

# 📃➡ Input Contents Format

Looking at the [`input.txt`](./input.txt) file, the contents are a list of integers (some negatives, but most are positives) separated by comas [`,`][w-comma].

# ⚙🚀 Implementation

## 💾🔍 Content Decoding

This encoding is identical to one used in [2019 day-2](../day-2), thus it is reused without any changes.

```python
def load_contents(filename: str) -> list[int]:
    contents = list(map(int, open(filename).read().strip().split(',')))
    return contents
```

## 💡🙋 Puzzle Solving

The solving process is simplified from day 2.

The first instruction: an `input` with opcode `0d3`, is hard coded before entering the iterative section.

```python
def execute_program(contents: list[int], input: int) -> int:
    instr_ptr = 0
    assert contents[instr_ptr] == 3
    contents[contents[1]] = input
    instr_ptr = 2
    output = -1
    while instr_ptr != -1:
        (instr_ptr, output) = execute(
            instr_ptr=instr_ptr, contents=contents, last_output=output)
    return output
```

```python
def execute(instr_ptr: int, contents: list[int], last_output: int) -> (int, int):
    instr = contents[instr_ptr]
    opcode = int(str(instr)[-2:])
    param_modes = decode_modes(instruction=instr)
    output = last_output
    arguments = list()
    for i, mode in enumerate(param_modes):
        argument = contents[instr_ptr + i + 1]
        position_mode = 0 == mode
        if position_mode:
            arguments.append(contents[argument])
        else:
            arguments.append(argument)
    if opcode == 1:
        result = sum(arguments[:-1])
        result_ptr = contents[instr_ptr + len(param_modes)]
        contents[result_ptr] = result
    elif opcode == 2:
        result = reduce(operator.mul, arguments[:-1], 1)
        result_ptr = contents[instr_ptr + len(param_modes)]
        contents[result_ptr] = result
    elif opcode == 3:
        raise Exception
    elif opcode == 4:
        output = arguments[0]
        log.info(f'output: {output}')
    elif opcode == 99:
        return -1, last_output
    next_instr = instr_ptr + INSTR_MAP[opcode]['length']
    return next_instr, output
```

Answer computation consists in using the last value assigned to the `output` variable.

```python
output = execute_program(contents=contents, input_=1)
return output
```

Contents | Answer
--- | ---
[`input.txt`](./input.txt) | `12234644`

# 😰🙅 Part Two

## 🥺👉👈 Annotated Description

> The air conditioner comes online! Its cold air feels good for a while, but then the TEST alarms start to go off. Since the air conditioner can't vent its heat anywhere but back into the spacecraft, it's actually making the air inside the ship warmer.
> 
> Instead, you'll need to use the TEST to extend the thermal radiators. Fortunately, the diagnostic program (your puzzle input) is already equipped for this. Unfortunately, your Intcode computer is not.

Meaning we can expect some new instructions!

> Your computer is only missing a few opcodes:
> 
>     Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
>     Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
>     Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
>     Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.

Jump instructions! This will require some refactoring!

Code | Operation | Total Length
--- | --- | ---
`5` | `jump-if-true` | `3`
`6` | `jump-if-false` | `3`
`7` | `less than` | `4`
`8` | `equals` | `4`

> Like all instructions, these instructions need to support parameter modes as described above.

Ok.

> Normally, after an instruction is finished, the instruction pointer increases by the number of values in that instruction. However, if the instruction modifies the instruction pointer, that value is used and the instruction pointer is not automatically increased.

Seems legit.

> For example, here are several programs that take one input, compare it to the value 8, and then produce one output:
> 
>     3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
>     3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
>     3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
>     3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
> 
> Here are some jump tests that take an input, then output 0 if the input was zero or 1 if the input was non-zero:
> 
>     3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
>     3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)
> 
> Here's a larger example:
> 
> 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
> 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
> 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
> 
> The above example program uses an input instruction to ask for a single number. The program will then output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8.
> 
> This time, when the TEST diagnostic program runs its input instruction to get the ID of the system to test, provide it 5, the ID for the ship's thermal radiator controller. This diagnostic test suite only outputs one number, the diagnostic code.
> 
> What is the diagnostic code for system ID 5?

## 🤔🤯 Solver Implementation

Work in part two consists in adding the four new instructions and processing logic.

```python
elif opcode == 5:
    non_zero = 0 != arguments[0]
    if non_zero:
        next_instr = arguments[1]
    else:
        next_instr = instr_ptr + INSTR_MAP[opcode]['length']
elif opcode == 6:
    zero = 0 == arguments[0]
    if zero:
        next_instr = arguments[1]
    else:
        next_instr = instr_ptr + INSTR_MAP[opcode]['length']
elif opcode == 7:
    less_than = arguments[0] < arguments[1]
    result_ptr = contents[instr_ptr + len(param_modes)]
    if less_than:
        contents[result_ptr] = 1
    else:
        contents[result_ptr] = 0
    next_instr = instr_ptr + INSTR_MAP[opcode]['length']
elif opcode == 8:
    equals = arguments[0] == arguments[1]
    result_ptr = contents[instr_ptr + len(param_modes)]
    if equals:
        contents[result_ptr] = 1
    else:
        contents[result_ptr] = 0
    next_instr = instr_ptr + INSTR_MAP[opcode]['length']
```

Contents | Answer
--- | ---
[`input.txt`](./input.txt) | `3508186`

# 🚀✨ Further Improvements 🚀✨

Several portions of the code could be refactored.

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-5]: https://adventofcode.com/2019/day/5

[py]: https://docs.python.org/3/
[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-counter]: https://docs.python.org/3/library/collections.html#collections.Counter
[py-exit]: https://docs.python.org/3/library/sys.html?highlight=sys%20exit#sys.exit
[py-generator]: https://docs.python.org/3/library/stdtypes.html#generator-types
[py-list]: https://docs.python.org/3/library/stdtypes.html#list
[py-main]: https://docs.python.org/3/library/__main__.html
[py-map]: https://docs.python.org/3/library/functions.html#map
[py-name]: https://docs.python.org/3/library/stdtypes.html#definition.__name__
[py-open]: https://docs.python.org/3/library/functions.html#open
[py-read]: https://docs.python.org/3/library/io.html#io.TextIOBase.read
[py-set]: https://docs.python.org/3/library/stdtypes.html#set
[py-split]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.split
[py-string]: https://docs.python.org/3/library/stdtypes.html#textseq
[py-strip]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
[py-sum]: https://docs.python.org/3/library/functions.html#sum
[py-tuple]: https://docs.python.org/3/library/stdtypes.html#tuple

[w-comma]: https://en.wikipedia.org/wiki/Comma#Computing
[w-newline]: https://en.wikipedia.org/wiki/Newline
[w-taxicab-geometry]: https://en.wikipedia.org/wiki/Taxicab_geometry
[w-distance]: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
