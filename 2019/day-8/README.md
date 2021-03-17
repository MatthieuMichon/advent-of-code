Solution in [Python][py] for the [day 8 puzzle][aoc-2019-8] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Space Image Format 🎄🌟🌟

# 🔍📖 Annotated Puzzle Statement

> The Elves' spirits are lifted when they realize you have an opportunity to reboot one of their Mars rovers, and so they are curious if you would spend a brief sojourn on Mars. You land your ship near the rover.

TIL a new word: `sojourn` 📚
```
sojourn (noun):
 - a temporary stay
   Middle English: from Old French sojourner, based on Latin sub- ‘under’ + late Latin diurnum ‘day’.
```

> When you reach the rover, you discover that it's already in the process of rebooting! It's just waiting for someone to enter a BIOS password. The Elf responsible for the rover takes a picture of the password (your puzzle input) and sends it to you via the Digital Sending Network.

Have a feeling this network reliability will turn out to be questionable.

> Unfortunately, images sent via the Digital Sending Network aren't encoded with any normal encoding; instead, they're encoded in a special Space Image Format. None of the Elves seem to remember why this is the case. They send you the instructions to decode it.

All long as these images are not animated.

> Images are sent as a series of digits that each represent the color of a single pixel. The digits fill each row of the image left-to-right, then move downward to the next row, filling rows top-to-bottom until every pixel of the image is filled.

So nothing too fancy for the moment.

> Each image actually consists of a series of identically-sized layers that are filled in this way. So, the first digit corresponds to the top-left pixel of the first layer, the second digit corresponds to the pixel to the right of that on the same layer, and so on until the last digit, which corresponds to the bottom-right pixel of the last layer.

Are we correct assuming these layers are stacked?

> For example, given an image `3` pixels wide and `2` pixels tall, the image data `123456789012` corresponds to the following image layers:
> 
> ```
> Layer 1: 123
>          456
> 
> Layer 2: 789
>          012
> ```

Ok this appears conspicuously easy, most likely I missed something.

> The image you received is `25` pixels wide and `6` pixels tall.
>
> To make sure the image wasn't corrupted during transmission, the Elves would like you to find the layer that contains the fewest 0 digits. On that layer, what is the number of 1 digits multiplied by the number of 2 digits?

Ok sounds fun!

# 📃➡ Input Contents Format

Input contents are characterized with three different attributes, listed in the table below.

Attribute | Type | Size | Description
--- | --- | --- | ---
Width | Integer | Several digits | Image width in pixels
Height | Integer | Several digits | Image height in pixels
Data | String | Up to 15'000 | Image pixels

The [Python][py] programming language comes with built-in [JSON] codec read methods such as [`json.load()`][py-json-load].

```json
{
  "width": 3,
  "height": 2,
  "data": "123456789012"
}
```

# ⚙🚀 Implementation

## 💾🔍 Content Decoding

With input contents being encoded in JSON decoding them is quite trivial. It is simply a mater of calling [`open()`][py-open] and passing the results to [`json.load()`][py-json-load].

```python
def load_contents(filename: str) -> map:
    contents = json.load(fp=open(filename))
    return contents
```

## 💡🙋 Puzzle Solving

The answer refers to a specific `layer`, meaning that the input data contents must be split into a number of layers.

> ... the Elves would like you to find the layer that contains the fewest 0 digits.

The data length of individual layers is known from start, making this operation easy to implement.

```python
def splice_data(data: str, width: int, height: int) -> list[str]:
    layer_length = width * height
    assert 0 == len(data) % layer_length
    layers = list()
    for i in range(0, len(data), layer_length):
        layers.append(data[i:i + layer_length])
    return layers
```

The following operation consists in finding the layer with the fewest number of 0 digits. The [`Counter`][py-counter] is well suited for this sort of computation.

```python
occurences = [collection.Counter(l) for l in layers]
```

Last action remaining is computing the index of the layer with the least quantity of zeros. And performing the final multiplication

```python
layer_least_zeroes = occurences.index(min(occurences))
layer_least_zeroes_occurence = Counter(layers[layer_least_zeroes])
answer = layer_least_zeroes_occurence['1'] * layer_least_zeroes_occurence['2']
```

Contents | Answer
--- | ---
[`example.txt`](./example.txt) | `1`
[`input.txt`](./input.txt) | `2064`


[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-8]: https://adventofcode.com/2019/day/8

[json]: https://www.json.org/json-en.html

[py]: https://docs.python.org/3/
[py-argparse]: https://docs.python.org/3/library/argparse.html
[py-copy]: https://docs.python.org/3/library/copy.html
[py-counter]: https://docs.python.org/3/library/collections.html#collections.Counter
[py-exit]: https://docs.python.org/3/library/sys.html?highlight=sys%20exit#sys.exit
[py-generator]: https://docs.python.org/3/library/stdtypes.html#generator-types
[py-json-load]: https://docs.python.org/3/library/json.html#json.load
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
