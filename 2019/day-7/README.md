Solution in [Python][py] for the [day 7 puzzle][aoc-2019-7] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Amplification Circuit 🎄🌟🌟

# 🔍📖 Annotated Statements

> Based on the navigational maps, you're going to need to send more power to your ship's thrusters to reach Santa in time. To do this, you'll need to configure a series of amplifiers already installed on the ship.

For some reason, this reminds me of *Moar Boosters!!!*.

> There are five amplifiers connected in series; each one receives an input signal and produces an output signal. They are connected such that the first amplifier's output leads to the second amplifier's input, the second amplifier's output leads to the third amplifier's input, and so on. The first amplifier's input value is 0, and the last amplifier's output leads to your ship's thrusters.

So we have five amplifiers in a [daisy chain][w-daisy-chain].

> ```
>     O-------O  O-------O  O-------O  O-------O  O-------O
> 0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
>     O-------O  O-------O  O-------O  O-------O  O-------O
> ```

So far so good.

> The Elves have sent you some Amplifier Controller Software (your puzzle input), a program that should run on your existing Intcode computer. Each amplifier will need to run a copy of the program.

Oh my, I must definitively improve the Intcode computer implementation.

> :memo: **Note**:
> 
> At the time when these lines were writen the Intcode computer implementation was quite crude.

We will go forward after checking the puzzle input and asses if rewriting the Intcode computer is required.

> When a copy of the program starts running on an amplifier, it will first use an input instruction to ask the amplifier for its current phase setting (an integer from 0 to 4). Each phase setting is used exactly once, but the Elves can't remember which amplifier needs which phase setting.

Ok so each amplifier stage takes an input argument ranging from 0 to 4. Each argument value is used exactly once.

We can be expected to compute the whole range of combinations.

> The program will then call another input instruction to get the amplifier's input signal, compute the correct output signal, and supply it back to the amplifier with an output instruction. (If the amplifier has not yet received an input signal, it waits until one arrives.)

Ok, so lets make that two inputs: a `phase setting` and a `input signal`.

> Your job is to find the largest output signal that can be sent to the thrusters by trying every possible combination of phase settings on the amplifiers. Make sure that memory is not shared or reused between copies of the program.

Thanks for the early warning!

> For example, suppose you want to try the phase setting sequence `3,1,2,4,0`, which would mean setting amplifier A to phase setting 3, amplifier B to setting 1, C to 2, D to 4, and E to 0. Then, you could determine the output signal that gets sent from amplifier E to the thrusters with the following steps:
> 
> * Start the copy of the amplifier controller software that will run on amplifier A. At its first input instruction, provide it the amplifier's phase setting, 3. At its second input instruction, provide it the input signal, 0. After some calculations, it will use an output instruction to indicate the amplifier's output signal.

The word `copy` is interesting, is this a hint to rely on the [`copy()`][py-copy] in disguise?

> * Start the software for amplifier B. Provide it the phase setting (1) and then whatever output signal was produced from amplifier A. It will then produce a new output signal destined for amplifier C. 
> * Start the software for amplifier C, provide the phase setting (2) and the value from amplifier B, then collect its output signal.
> * Run amplifier D's software, provide the phase setting (4) and input value, and collect its output signal.
> * Run amplifier E's software, provide the phase setting (0) and input value, and collect its output signal.

Ok doesn't appear too bad?!

*famous last words*

> The final output signal from amplifier E would be sent to the thrusters. However, this phase setting sequence may not have been the best one; another sequence might have sent a higher signal to the thrusters.

Alright!

> Here are some example programs:
> 
> ```
>    Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):
>
>    3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
>
>    Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):
>
>    3,23,3,24,1002,24,10,24,1002,23,-1,23,
>    101,5,23,23,1,24,23,23,4,23,99,0,0
>
>    Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):
>
>    3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
>    1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
> ```

So many examples... would be easier to pack several inputs in a single file?

> Try every combination of phase settings on the amplifiers. What is the highest signal that can be sent to the thrusters?

We figured so much!

# 📃➡ Input Contents Format

First thing when having to design an input decoder is to understand how input contents are structured.

For instance the puzle input contents fit on a single line of text, whereas we have several examples meaning several lines. The smart thing to do would be to handle both.

Input | Lines | Total Length
--- | --- | ---
[`examples.txt`](./examples.txt) | 3 | 76
[`input.txt`](./input.txt) | 1 | 523

Looking into the contents themselves, they consist in one or more lines listing a series of integers separated by [`coma`][w-comma]: `,` characters. 

# ⚙🚀 Implementation

## 💾🔍 Content Decoding

The most convenient format for the objects returned from the `load_contents()` method handling content decoding is a nested [list][py-list] of integers.

Doing so allows yielding several answers from a single file, as it is the case with the [`examples.txt`](./examples.txt) file.

Starting from a filename encoded as a [`str`][py-string] object, the following sequence of operations are required:

1. Open and read the file, with the usual [`open()`][py-open] and [`read()`][py-read] methods.
1. Remove the trailing line return, using [`strip()`][py-strip].
1. Split the single string into a [`list`][py-list] of strings using [`split()`][py-split] on new line boundaries with [`os.linesep`][py-linesep].
1. For each item of the list of strings
    1. Split the string using the [`coma`][w-comma] character as separator.
    1. Convert numbers in string into integers using the [`map()`][py-map] method, while casting them into a list.

Translating these steps into source code yields the following:

```python
def load_contents(filename: str) -> list[list[int]]:
    lines = open(filename).read().strip().split(os.linesep)
    contents = [list(map(int, l.split(','))) for l in lines]
    return contents
```

## 💡🙋 Puzzle Solving

As usual I opted to rely on a several layers of methods for solving this puzzle. The first one is a high-level `solve()` method. This method takes a single list of `Intcode` data a executes a couple of steps.

> :memo: **Note**:
> 
> Some steps could be fused together, but for clarity are executed a part.

1. Initialize a `amp_outputs` list receiving per-combination output values.
2. Pre-computes all `phase settings` combinations. The [`intertools`][py-itertools] library provides the [`permutations()`][py-itertools-permutations] which matches our use case.

```python
    phase_settings = itertools.permutations(
        iterable=range(*PHASE_RANGE), r=AMPLIFIERS)
```

2. Iterate for each `phase setting`
   1. Clear `amp_input` value.
   1. Iterate for each amplifier stage
      1. Get the relevant `phase setting` from the list for the current stage.
      1. Get a fresh copy of the `Intcode` contents, as it is likely they will be modified.
      1. Call a method, `compute_output_signal()` executing the `Intcode` contents and yielding the output for the given amplifier stage.
      1. Loop the output to the input value
   1. Append to final output value after going through all amplifier stages.

```python
 for phase_setting in phase_settings:
     amp_input = 0
     amp_output = 0
     for amp in range(AMPLIFIERS):
         amp_phase_setting = phase_setting[amp]
         temp_contents = contents.copy()
         amp_output = compute_output_signal(
             data=temp_contents, input_=amp_input,
             phase=amp_phase_setting)
         amp_input = amp_output
     amp_outputs.append(amp_output)
```

The `compute_output_signal()` computes the computation of the output yielded by a single amplifier stage. It serializes input values retrieved by the `RD` instructions and execute instructions, stopping only when a `HALT` instruction is encountered.

```python
def compute_output_signal(data: list[int], input_: int, phase: int) -> int:
    inputs = [phase, input_]
    opcode_ptr: int = 0
    output: int = 0
    while data[opcode_ptr] != Intcode.HALT:
        opcode_ptr, inputs, output = execute_opcode(
            data=data, opcode_ptr=opcode_ptr, inputs=inputs)
    return output
```

The `execute_opcode()` does the heavy-lifting:

1. Fetches the instruction for the given opcode pointer.
1. Decodes the instruction into: an opcode; and a list of per-argument parameter modes.
1. Fetches input argument values depending on their corresponding parameter modes.
1. Executes the opcode.
   * If relevant, computes the pointer to the output value.
   * If relevant, computes the output value and assigns via the pointer.
   * Computes the new opcode pointer value.
1. Returns a list of the opcode pointer value; input values lists; output value.

```python
def execute_opcode(data: list[int], opcode_ptr: int,
                   inputs: list[int]) -> [int, list[int], any]:
    instruction = data[opcode_ptr]
    opcode, parameter_modes = decode_instruction(instruction)
    assert Intcode(opcode) in opcode_map
    opcode_args = fetch_arguments(data=data, opcode_ptr=opcode_ptr,
                                  parameter_modes=parameter_modes)
    output = None
    if opcode == Intcode.ADD:
        ...
    elif opcode == Intcode.MUL:
        ...
    ...
    elif opcode == Intcode.HALT:
        raise Exception
    return opcode_ptr, inputs, output
```

Computing the output is simply a matter of getting the highest output value at the end of the `solve()` method.

```python
 answer = max(amp_outputs)
 return answer
```

Contents | Answer
--- | ---
[`examples.txt`](./examples.txt) | `[43210, 54321, 65210]`
[`input.txt`](./input.txt) | `118936`

# 😰🙅 Part Two

## 🥺👉👈 Annotated Description

> It's no good - in this configuration, the amplifiers can't generate a large enough output signal to produce the thrust you'll need. The Elves quickly talk you through rewiring the amplifiers into a feedback loop:
> ```
>       O-------O  O-------O  O-------O  O-------O  O-------O
> 0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
>    |  O-------O  O-------O  O-------O  O-------O  O-------O |
>    |                                                        |
>    '--------------------------------------------------------+
>                                                             |
>                                                             v
>                                                      (to thrusters)
> ```

Oh, a feedback loop, this can't be good...

> Most of the amplifiers are connected as they were before; amplifier A's output is connected to amplifier B's input, and so on. However, the output from amplifier E is now connected into amplifier A's input. This creates the feedback loop: the signal will be sent through the amplifiers many times.

*Many times*, seems like things will get real.

> In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9, again each used exactly once. These settings will cause the Amplifier Controller Software to repeatedly take input and produce output many times before halting. Provide each amplifier its phase setting at its first input instruction; all further input/output instructions are for signals.

A different range for the phase settings shouldn't be a problem.

> Don't restart the Amplifier Controller Software on any amplifier during this process. Each one should continue receiving and sending signals until it halts.

Saving the software state per-stage will require some notable changes.

> All signals sent or received in this process will be between pairs of amplifiers except the very first signal and the very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once.

Seems logical.

> Eventually, the software on the amplifiers will halt after they have processed the final loop. When this happens, the last output signal from amplifier E is sent to the thrusters. Your job is to find the largest output signal that can be sent to the thrusters using the new phase settings and feedback loop arrangement.

This match the behavior from part one.

Here are some example programs:

> Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):
>
> ```
> 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
>   27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
> ```
> 
> Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):
> 
> ```
> 3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
>   -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
>   53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
> ```

Just some examples, which will require a new [`examples_part_two.txt`](./examples_part_two.txt) file.

> Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that can be sent to the thrusters?

The answer to be computed remains the same.

## 🤔🤯 Solver Implementation

The puzzle states about the *Amplifier Controller Software* that it must not be restarted, instead it should be continue receiving and sending signals until it halts. This requires creating a list of such software instructions for each amplifier stage.

```python
per_stage_software = [contents.copy() for _ in range(AMPLIFIERS)]
```

Furthermore, the current instruction pointer must be saved for each amplifier stage.

> :ng: **Unexpected Behavior**:
> 
> A first implementation of the part two solver `solve_part_two()`, although yielded the expected values when run against the [`examples_part_two.txt`](./examples_part_two.txt), produced invalid results on the [`input.txt`](./input.txt) file. 

```python
# 250 - solve_part_two                   - DEBUG    - iter #40, stage 0: iptr 514, output 28019459
# 250 - solve_part_two                   - DEBUG    - iter #41, stage 1: iptr 352, output 28019461
# 250 - solve_part_two                   - DEBUG    - iter #42, stage 2: iptr 433, output 28019463
# 250 - solve_part_two                   - DEBUG    - iter #43, stage 3: iptr 190, output 28019465
# 250 - solve_part_two                   - DEBUG    - iter #44, stage 4: iptr 271, output 56038930
# 250 - solve_part_two                   - DEBUG    - iter #45, stage 0: iptr 522, output 56038931
# 250 - solve_part_two                   - DEBUG    - iter #46, stage 1: iptr 360, output 56038933
# 250 - solve_part_two                   - DEBUG    - iter #47, stage 2: iptr 441, output 56038934
# 250 - solve_part_two                   - DEBUG    - iter #48, stage 3: iptr 198, output 56038935
# 250 - solve_part_two                   - DEBUG    - iter #49, stage 4: iptr 279, output 56038936
# 250 - solve_part_two                   - DEBUG    - iter #50, stage 0: iptr 522, output 0
# 250 - solve_part_two                   - DEBUG    - iter #51, stage 1: iptr 360, output 0
# 250 - solve_part_two                   - DEBUG    - iter #52, stage 2: iptr 441, output 0
# 250 - solve_part_two                   - DEBUG    - iter #53, stage 3: iptr 198, output 0
# 250 - solve_part_two                   - DEBUG    - iter #54, stage 4: iptr 279, output 0
```

Issue is likely to be related to the last feedback loop, during which all stages terminated reaching an halt instruction and yielded the value zero.

The end of the Intcode sequence differs between the examples and the input:

```
# input.txt
   ...,101,1,9,9,4,9,99

# examples_part_two.txt
   ...,1005,28,6,99,0,0,5
   ...,1005,56,6,99,0,0,0,0,10
```

The [`input.txt`](./input.txt) file finishes with the `HALT` instruction, which is not the case with both inputs of the [`examples_part_two.txt`](./examples_part_two.txt).

Tracing back this zero value leads to `compute_output_signal()` which upon processing a single `HALT` instruction will shortcut and return with `output` set to `0` 🤦

The correction turns out to be trivial.
```diff
     else:
         inputs = [input_]
     opcode_ptr: int = instruction_ptr
-    output: int = 0
+    output = None
     while data[opcode_ptr] != Intcode.HALT:
         opcode_ptr, inputs, output = execute_opcode(
             data=data, opcode_ptr=opcode_ptr, inputs=inputs)
```

Contents | Answer
--- | ---
[`examples_part_two.txt`](./examples.txt) | `[139629729, 18216]`
[`input.txt`](./input.txt) | `57660948`

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-7]: https://adventofcode.com/2019/day/7

[py]: https://docs.python.org/3/
[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-copy]: https://docs.python.org/3/library/copy.html
[py-counter]: https://docs.python.org/3/library/collections.html#collections.Counter
[py-exit]: https://docs.python.org/3/library/sys.html?highlight=sys%20exit#sys.exit
[py-generator]: https://docs.python.org/3/library/stdtypes.html#generator-types
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
[py-set]: https://docs.python.org/3/library/stdtypes.html#set
[py-split]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.split
[py-string]: https://docs.python.org/3/library/stdtypes.html#textseq
[py-strip]: https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip
[py-sum]: https://docs.python.org/3/library/functions.html#sum
[py-tuple]: https://docs.python.org/3/library/stdtypes.html#tuple

[w-comma]: https://en.wikipedia.org/wiki/Comma#Computing
[w-daisy-chain]: https://en.wikipedia.org/wiki/Daisy_chain_(electrical_engineering)
[w-distance]: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
[w-newline]: https://en.wikipedia.org/wiki/Newline
[w-taxicab-geometry]: https://en.wikipedia.org/wiki/Taxicab_geometry
