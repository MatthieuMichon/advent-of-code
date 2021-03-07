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

Input | Lines
--- | ---
[`examples.txt`](./examples.txt) | `3`
[`input.txt`](./input.txt) | `1`

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
[py-list]: https://docs.python.org/3/library/stdtypes.html#list
[py-main]: https://docs.python.org/3/library/__main__.html
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
