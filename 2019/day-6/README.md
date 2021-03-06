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

Starting from a filename encoded as a [`str`][py-string] object, the following sequence of operations are required:

1. Open and read the file, with the usual [`open()`][py-open] and [`read()`][py-read] methods.
1. Remove the trailing line return, using [`strip()`][py-strip].
1. Split the single string into a [`list`][py-list] of strings using [`split()`][py-split] on new line boundaries with [`os.linesep`][py-linesep].
1. For each item of the list of strings
    1. Split the string using a closing parenthesis `)` as separator.

```python
def load_contents(filename: str) -> list[tuple]:
    lines = open(filename).read().strip().split(os.linesep)
    contents = [tuple(l.split(')')) for l in lines]
    return contents
```

## 💡🙋 Puzzle Solving

The answer as stated in the puzzle, consists in the total of direct and indirect orbits.

> What is the total number of direct and indirect orbits in your map data?

Direct orbits correspond to the contents extracted from the input file. The indirect orbits require to compute all the paths between objects separated by distance of two or greater.

A first brute force approach to this problem would consist in building a per-object map which points to a list of other objects it relates to. The algorithm in this case requires computing a map of objects which orbit another object, which is the reverse of the contents extracted from the file.

1. Initialize a new map.
1. For each (`orbited`, `orbiter`) tuple in the content list.
    1. Create a new `orbiter` entry in the map referencing the `orbited` object.

```python
orbiters = dict()
for orbited, orbiter in contents:
    orbiters[orbiter] = orbited
```

The next step consists in expanding all the possible dependencies.

1. Initialize a new map.
1. For each orbiter in the `orbiters` map
    1. Expand the list of orbited objects.

The expansion of an object into the list of all objects it orbits around is easier done using a recursive method, taking the `orbiters` along a single `orbiter`, and returns a list of objects.

1. Initialize an empty list.
1. Lookup the object around which the `orbiter` orbits around.
1. Append the orbited object to the list.
1. Test if the orbited object is equal to `COM`, the *universal Center of Mass*:
    * If not equal, then call again this method and append its result to the list before returning it.
1. Return the list of orbited objects.

```python
COM = 'COM'

def expand_orbited_objects(orbiters: list[tuple], orbiter: str) -> list[str]:
    orbited_objects = list()
    orbited = orbiters[orbiter]
    orbited_objects.append(orbited)
    if COM != orbited:
       orbited_objects.extend(expand_orbited_objects(orbiters, orbited))
    return orbited_objects
```

Computing the answer is just a mater of counting all the items for all the orbiters.

```python
answer = sum(len(v) for v in orbited_objects.values())
```

The solving method pieced together:

```python
def solve(contents: list[tuple]) -> int:
    orbiters = dict()
    for orbited, orbiter in contents:
        orbiters[orbiter] = orbited
    orbited_objects = dict()
    for orbiter in orbiters:
        orbited_objects[orbiter] = expand_orbited_objects(
            orbiters=orbiters, orbiter=orbiter)
    output = sum(len(v) for v in orbited_objects.values())
    return output
```

Contents | Answer
--- | ---
[`example.txt`](./input.txt) | `42`
[`input.txt`](./input.txt) | `151345`


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
[py-linesep]: https://docs.python.org/3/library/os.html#os.linesep
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
