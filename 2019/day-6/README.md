Solution in [Python][py] for the [day 6 puzzle][aoc-2019-6] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Universal Orbit Map 🎄🌟🌟

# 🔍📖 Annotated Statements

> You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves transferring between orbits, the orbit maps here are useful for finding efficient routes between, for example, you and Santa. You download a map of the local orbits (your puzzle input).

Backstory introduction.

> Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object. An orbit looks roughly like this:
> 
> ```
>                   \
>                    \
>                     |
>                     |
> AAA--> o            o <--BBB
>                     |
>                     |
>                    /
>                   /
> ```
> 
> In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is only partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit around AAA".

No questions yet.

> Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits (like the one shown above) and indirect orbits.

What are these indirect orbits?

> Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.

Example:

Body | Example
--- | ---
`A` | Moon
`B` | Earth
`C` | Sun
`D` | Galactic Center

> For example, suppose you have the following map:
> 
> ```
> COM)B
> B)C
> C)D
> D)E
> E)F
> B)G
> G)H
> D)I
> E)J
> J)K
> K)L
> ```
> 
> Visually, the above map of orbits looks like this:
> 
> ```
>         G - H       J - K - L
>        /           /
> COM - B - C - D - E - F
>                \
>                 I
> ```
> 
> In this visual representation, when two objects are connected by a line, the one on the right directly orbits the one on the left.
> 
> Here, we can count the total number of orbits as follows:
> 
>     D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
>     L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
>     COM orbits nothing.
> 
> The total number of direct and indirect orbits in this example is 42.

Computing the number of orbits can be compared as a graph traversal. 

> What is the total number of direct and indirect orbits in your map data?

Indeed.

# 📃➡ Input Contents Format

Content files, [`example.txt`](./example.txt) and [`input.txt`](./input.txt), contain a number of lines with two alphanumeric identifiers separated by a single closing parenthesis.

# ⚙🚀 Implementation

## 💾🔍 Content Decoding

The most practical output format after decoding will be a list of tuples. Each tuple representing a pair of objects, the second one orbiting the first one.

Thus, we need the [`open()`][py-open]; [`read()`][py-read]; [`strip()`][py-strip] and [`split()`][py-split] methods.

```python
def load_contents(filename: str) -> list[tuple]:
    lines = open(filename).read().strip().split(os.linesep)
    contents = [tuple(l.split(')')) for l in lines]
    return contents
```

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-6]: https://adventofcode.com/2019/day/6

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
