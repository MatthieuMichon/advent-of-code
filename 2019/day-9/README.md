Solution in [Python][py] for the [day 9 puzzle][aoc-2019-9] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Sensor Boost 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> You've just said goodbye to the rebooted rover and left Mars when you receive a faint distress signal coming from the asteroid belt. It must be the Ceres monitoring station!

Can only be aliens!

> In order to lock on to the signal, you'll need to boost your sensors. The Elves send up the latest BOOST program - Basic Operation Of System Test.

Kudos bright Elves!

> While BOOST (your puzzle input) is capable of boosting your sensors, for tenuous safety reasons, it refuses to do so until the computer it runs on passes some checks to demonstrate it is a complete Intcode computer.

Computer security at its finest!

> Your existing Intcode computer is missing one key feature: it needs support for parameters in relative mode.

Improving Intcode is always a win.

> Parameters in mode 2, relative mode, behave very similarly to parameters in position mode: the parameter is interpreted as a position. Like position mode, parameters in relative mode can be read from or written to.

Adding this new mode leaves us with the following values:

Value | Mode Name | Description
--- | --- | ---
0 | Position mode | Parameter is addressed through a pointer 
1 | Immediate mode | Parameter is the instruction argument 
2 | Relative mode | Parameter is addressed through a pointer computed with an offset

> The important difference is that relative mode parameters don't count from address 0. Instead, they count from a value called the relative base. The relative base starts at 0.
> 
> The address a relative mode parameter refers to is itself plus the current relative base. When the relative base is 0, relative mode parameters and position mode parameters with the same value refer to the same address.

Figured so much.

> For example, given a relative base of 50, a relative mode parameter of -7 refers to memory address 50 + -7 = 43.
> 
> The relative base is modified with the relative base offset instruction:
> 
> * Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases (or decreases, if the value is negative) by the value of the parameter.
> 
> For example, if the relative base is 2000, then after the instruction 109,19, the relative base would be 2019. If the next instruction were 204,-34, then the value at address 1985 would be output.

Examples for unitary tests, always nice.

> Your Intcode computer will also need a few other capabilities:
> 
> * The computer's available memory should be much larger than the initial program. Memory beyond the initial program starts with the value 0 and can be read or written like any other memory. (It is invalid to try to access memory at a negative address, though.)
> * The computer should have support for large numbers. Some instructions near the beginning of the BOOST program will verify this capability.

Always nice to know beforehand.

> Here are some example programs that use these features:
> 
> * 109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and produces a copy of itself as output.
> * 1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
> * 104,1125899906842624,99 should output the large number in the middle.

More examples.

> The BOOST program will ask for a single input; run it in test mode by providing it the value 1. It will perform a series of checks on each opcode, output any opcodes (and the associated parameter modes) that seem to be functioning incorrectly, and finally output a BOOST keycode.

Ok so executing the program with `1` as an input yields a keycode.

> Once your Intcode computer is fully functional, the BOOST program should report no malfunctioning opcodes when run in test mode; it should only output a single value, the BOOST keycode. What BOOST keycode does it produce?

Executing again the program with the keycode as an input yields the answer, got it!

## 💾🔍 Content Decoding

As the name implies, this puzzle input consists in *Intcode*. Accordingly, expected contents coming out of the decoder is a list of integers. For a change the `load_contents()` method relies on a [`iterator`][py-iterator] instead of using a plain [`return`][py-return] statement. 

The method yields a single list of integers depending on the number of lines, allowing for packing all examples in a single file.

```python
def load_contents(filename: str) -> Iterator[list[int]]:
    lines = open(filename).read().strip().split(os.linesep)
    for line in lines:
        yield [int(token) for token in line.split(',')]
```

## 💡🙋 Puzzle Solver

Because we can and ftw, I'm in the mood of trying something different rather than plainly copy / pasting code from day 5.

Thus [ISA][w-isa] details are stored in a `ISA` map. Each map entries points to a [`SimpleNamespace`][py-sn] instance, encoding information listed below.

Entry | Description
--- | ---
`name` | Human readable name
`input_args` | number of arguments popped from the `inputs` list
`load_args` | number of arguments loaded by the instruction
`store_args` | number of arguments stored by the instruction
`output_args` | number of arguments pushed in the `outputs` list

```python
from types import SimpleNamespace as sn

ISA = {
    2: sn(name='Add', input_args=0, load_args=2, store_args=1, output_args=0),
}
```

The first methode is `decode()` converting an instruction into its opcode and list modes applying to its loaded arguments.

```python
INTCODE_INSTR_MOD = 100

def decode(instruction: int) -> [int, list[int]]:
    opcode = instruction % INTCODE_INSTR_MOD
    if opcode not in ISA:
        raise OpcodeError(opcode)
    loaded_args = ISA[opcode].load_args
    modes_int = instruction // INTCODE_INSTR_MOD
    modes = [Mode(int(m)) for m in reversed(str(modes_int))]
    leading_zero_modes = [Mode.IMMEDIATE] * (loaded_args - len(modes))
    padded_modes = modes + leading_zero_modes
    return opcode, padded_modes
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
[aoc-2019-9]: https://adventofcode.com/2019/day/9

[json]: https://www.json.org/json-en.html

[py]: https://docs.python.org/3/
[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-copy]: https://docs.python.org/3/library/copy.html
[py-counter]: https://docs.python.org/3/library/collections.html#collections.Counter
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
