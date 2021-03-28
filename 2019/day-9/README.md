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

Thus [ISA] details are stored in a `ISA` map. Each map entries points to a [`SimpleNamespace`][py-sn] instance, encoding information listed below.

Entry | Description
--- | ---
`name` | Human readable name
`input_args` | number of arguments popped from the `inputs` list
`load_args` | number of arguments loaded by the instruction
`store_args` | number of arguments stored by the instruction
`output_args` | number of arguments pushed in the `outputs` list
`jump` | boolean indicating if the instruction may override the instruction pointer

```python
from types import SimpleNamespace as sn

ISA = {
    1: sn(name='Add', input_args=0, load_args=2, store_args=1, output_args=0, jump=False),
    # ...
    99: sn(name='Halt', input_args=0, load_args=0, store_args=0, output_args=0, jump=False),
}
```

Opcode | Mnemonic | Name | Input Args | Load Args | Store Args | Output Args | Jump
--- | --- | --- | --- | --- | --- | --- | ---
`1` | `Add` | Add | 0 | 2 | 1 | 0 | ❌
`2` | `Mul` | Multiply | 0 | 2 | 1 | 0 | ❌
`3` | `In` | Read input value | 1 | 0 | 1 | 0 | ❌
`4` | `Out` | Write output value | 0 | 1 | 0 | 1 | ❌
`5` | `JNZ` | Jump if non-zero | 0 | 2 | 0 | 0 | ✔️
`6` | `JZ` | Jump if zero | 0 | 2 | 0 | 0 | ✔️
`7` | `LT` | Assign if lower | 0 | 2 | 1 | 0 | ❌
`8` | `Eq` | Assign if equal | 0 | 2 | 1 | 0 | ❌
`9` | `RBS` | Shift `relative_base` value  | 0 | 1 | 0 | 0 | ❌
`99` | `Halt` | Halt processing  | 0 | 0 | 0 | 0 | ❌

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

> :ng: **Unexpected Behavior**:
> 
> The first implementation was operating under the assumption stated in day 5:
> 
> ```
> Parameters that an instruction writes to will never be in immediate mode.
> ```
> 
> It turns out that such parameters (named `stored operand` in my implementation) can be in modes different from the immediate mode. Thankfully this issue was pointed out in the list of instructions being incorrectly implemented.
> Furthermore a bug affects the `leading_zero_modes` variable, which was duplicating `Mode.IMMEDIATE` instead of `Mode.POSITION`.

The correct `decode()` method now being:

```python
def decode(instruction: int) -> [int, list[int]]:
    opcode = instruction % INTCODE_INSTR_MOD
    if opcode not in ISA:
        raise OpcodeError(opcode=opcode)
    args_qty = ISA[opcode].load_args + ISA[opcode].store_args
    modes_int = instruction // INTCODE_INSTR_MOD
    modes = [Mode(int(m)) for m in reversed(str(modes_int))]
    leading_zero_modes = [Mode.POSITION] * (args_qty - len(modes))
    padded_modes = modes + leading_zero_modes
    return opcode, padded_modes
```

The processing pipeline is broken in the usual steps, starting with the *fetch* stage.

```python
def fetch(
        instruction_pointer: int,
        load_modes: list[int],
        ram: dict[int, int],
        relative_base: int,
        opcode:int,
        input_stack: list[int]) -> list[int]:
    operands = list()
    if ISA[opcode].input_args > 0:
        for _ in range(ISA[opcode].input_args):
            operands.append(input_stack.pop())
    else:
        for i, mode in enumerate(load_modes):
            pointer = instruction_pointer + 1 + i
            contents = ram[pointer]
            if mode == Mode.IMMEDIATE:
                operands.append(contents)
            elif mode == Mode.POSITION:
                operands.append(ram.get(contents, DEFAULT_RAM_VALUE))
            elif mode == Mode.RELATIVE:
                operands.append(ram[relative_base + contents])
            else:
                raise Exception
    return operands
```

Next up is `execute()`, nothing fancy here.

```python
def execute(opcode:int , operands: list[int]) -> int:
    result = None
    if ISA[opcode].name == 'Add':
        result = sum(operands)
    if ISA[opcode].name == 'Mul':
        result = operands[0] * operands[1]
    if ISA[opcode].name == 'In':
        result = operands[0]
    if ISA[opcode].name == 'Out':
        result = operands[0]
    if ISA[opcode].name == 'LT':
        result = 1 if operands[0] < operands[1] else 0
    if ISA[opcode].name == 'Eq':
        result = 1 if operands[0] == operands[1] else 0
    if ISA[opcode].name == 'JNZ':
        result = operands[1]
    if ISA[opcode].name == 'JZ':
        result = operands[1]
    if ISA[opcode].name == 'RBS':
        result = operands[0]
    assert result is not None
    return result
```

The store() method however had to be updated for handling different result operand modes.

> :memo: **Note**:
> 
> For some reason, there are no stored arguments using the *immediate mode*.

```python
def store(
        opcode: int,
        store_mode: int,
        output: int,
        instruction_pointer: int,
        ram: dict[int, int],
        relative_base: int) -> None:
    no_store = ISA[opcode].store_args == 0
    if no_store:
        return
    if store_mode == Mode.RELATIVE:
        store_pointer_address = instruction_pointer + 1 + ISA[opcode].load_args
        store_pointer = relative_base + ram.get(store_pointer_address, DEFAULT_RAM_VALUE)
    elif store_mode == Mode.POSITION:
        store_pointer_address = instruction_pointer + 1 + ISA[opcode].load_args
        store_pointer = ram[store_pointer_address]
    else:
        raise Exception
    ram[store_pointer] = output
    return
```

The remaining methods deal with updating the rest of the internal state.

```python
def push_output(opcode: int, output: int) -> list[int]:
    output_ = list()
    if ISA[opcode].name == 'Out':
        output_.append(output)
    return output_
```

```python
def shift_base(opcode: int, output: int) -> int:
    shift = 0
    if ISA[opcode].name == 'RBS':
        shift = output
    return shift
```

```python
def jump_next_instruction(
        opcode: int,
        instruction_pointer: int,
        operands: list[int], output: int) -> int:
    next_instruction = instruction_pointer + 1 + \
                       ISA[opcode].load_args + ISA[opcode].store_args
    if ISA[opcode].name in ['Add', 'Mul', 'RBS', 'LT', 'Eq', 'In', 'Out']:
        pass
    elif ISA[opcode].name == 'JNZ':
        non_zero = operands[0] != 0
        next_instruction = operands[1] if non_zero else next_instruction
    elif ISA[opcode].name == 'JZ':
        non_zero = operands[0] == 0
        next_instruction = operands[1] if non_zero else next_instruction
    else:
        raise Exception
    return next_instruction
```

Finally all these methods are orchestrated by an `execute_program()` function.

```python
def execute_program(
        ram: dict[int, int],
        instruction_pointer: int,
        input_stack: list[int]) -> list[int]:
    output_values = list()
    relative_base = 0
    while True:
        instruction = ram[instruction_pointer]
        opcode, operand_modes = decode(instruction=instruction)
        halt = ISA[opcode].name == 'Halt'
        if halt:
            break
        load_modes = operand_modes[:ISA[opcode].load_args]
        operands = fetch(instruction_pointer=instruction_pointer,
                         load_modes=load_modes, ram=ram,
                         relative_base=relative_base,
                         opcode=opcode, input_stack=input_stack)
        output = execute(opcode=opcode, operands=operands)
        store_mode = operand_modes[-ISA[opcode].store_args:][0]
        store(opcode=opcode, store_mode=store_mode, output=output,
              instruction_pointer=instruction_pointer, ram=ram,
              relative_base=relative_base)
        output_values.extend(push_output(opcode=opcode, output=output))
        relative_base += shift_base(opcode=opcode, output=output)
        next_instruction_pointer = jump_next_instruction(
            opcode=opcode, instruction_pointer=instruction_pointer,
            operands=operands, output=output)
        instruction_pointer = next_instruction_pointer
    return output_values
```

Contents | Answer
--- | ---
[`input.txt`](./input.txt) | `[3497884671]`

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

> You now have a complete Intcode computer.

All right, let's get things done!

> Finally, you can lock on to the Ceres distress signal! You just need to boost your sensors using the BOOST program.
> 
> The program runs in sensor boost mode by providing the input instruction the value `2`. Once run, it will boost the sensors automatically, but it might take a few seconds to complete the operation on slower hardware. In sensor boost mode, the program will output a single value: the coordinates of the distress signal.

A *few seconds*?! Heard of this one before!

> Run the BOOST program in sensor boost mode. What are the coordinates of the distress signal?

## 🤔🤯 Puzzle Solver

Thanks to using a hash-table along with `get()` methods for accessing *clean* addresses, the second part is solved after just a few seconds!

Contents | Answer
--- | ---
[`input.txt`](./input.txt) | `[46470]`

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
