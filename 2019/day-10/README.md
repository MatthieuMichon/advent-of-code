Solution in [Python][py] for the [day 10 puzzle][aoc-2019-10] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Monitoring Station 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> You fly into the asteroid belt and reach the Ceres monitoring station. The Elves here have an emergency: they're having trouble tracking all of the asteroids and can't be sure they're safe.
> 
> The Elves would like to build a new monitoring station in a nearby area of space; they hand you a map of all of the asteroids in that region (your puzzle input).
> 
> The map indicates whether each position is empty (.) or contains an asteroid (#). The asteroids are much smaller than they appear on the map, and every asteroid is exactly in the center of its marked position. The asteroids can be described with X,Y coordinates where X is the distance from the left edge and Y is the distance from the top edge (so the top-left corner is 0,0 and the position immediately to its right is 1,0).

Origin is top-left corner.

> Your job is to figure out which asteroid would be the best place to build a new monitoring station. A monitoring station can detect any asteroid to which it has direct line of sight - that is, there cannot be another asteroid exactly between them. This line of sight can be at any angle, not just lines aligned to the grid or diagonally. The best location is the asteroid that can detect the largest number of other asteroids.

The `line of sight can be at any angle` makes things much more interesting, which is further confirmed with `not just lines aligned to the grid or diagonally`. This will require some thinking.

> For example, consider the following map:
> 
> ```
> .#..#
> .....
> #####
> ....#
> ...##
> ```
> 
> The best location for a new monitoring station on this map is the highlighted asteroid at 3,4 because it can detect 8 asteroids, more than any other location. (The only asteroid it cannot detect is the one at 1,0; its view of this asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse locations; they can detect 7 or fewer other asteroids. Here is the number of other asteroids a monitoring station on each asteroid could detect:
> 
> ```
> .7..7
> .....
> 67775
> ....7
> ...87
> ```

Example makes sense.

> Here is an asteroid (#) and some examples of the ways its line of sight might be blocked. If there were another asteroid at the location of a capital letter, the locations marked with the corresponding lowercase letter would be blocked and could not be detected:
> 
> ```
> #.........
> ...A......
> ...B..a...
> .EDCG....a
> ..F.c.b...
> .....c....
> ..efd.c.gb
> .......c..
> ....f...c.
> ...e..d..c
> ```

This examples hints at a possible implementation, overlay aliasing positions of an asteroid and mark those as empty. 

> Here are some larger examples:
> 
> *Best is 5,8 with 33 other asteroids detected:*
> 
> ```
> ......#.#.
> #..#.#....
> ..#######.
> .#.#.###..
> .#..#.....
> ..#....#.#
> #..#....#.
> .##.#..###
> ##...#..#.
> .#....####
> ```
> 
> *Best is 1,2 with 35 other asteroids detected:*
> 
> ```
> #.#...#.#.
> .###....#.
> .#....#...
> ##.#.#.#.#
> ....#.#.#.
> .##..###.#
> ..#...##..
> ..##....##
> ......#...
> .####.###.
> ```
> 
> *Best is 6,3 with 41 other asteroids detected:*
> 
> ```
> .#..#..###
> ####.###.#
> ....###.#.
> ..###.##.#
> ##.##.#.#.
> ....###..#
> ..#.#..#.#
> #..#.#.###
> .##...##.#
> .....#.#..
> ```
> 
> *Best is 11,13 with 210 other asteroids detected:*
> 
> ```
> .#..##.###...#######
> ##.############..##.
> .#.######.########.#
> .###.#######.####.#.
> #####.##.#.##.###.##
> ..#####..#.#########
> ####################
> #.####....###.#.#.##
> ##.#################
> #####.##.###..####..
> ..######..##.#######
> ####.##.####...##..#
> .#####..#.######.###
> ##...#.##########...
> #.##########.#######
> .####.#.###.###.#.##
> ....##.##.###..#####
> .#.#.###########.###
> #.#.#.#####.####.###
> ###.##.####.##.#..##
> ```
> 
> Find the best location for a new monitoring station. How many other asteroids can be detected from that location?

Puzzle answer is as shown in the previous examples.

## 💾🔍 Content Decoding

We start with these simple requirements:

* Storing all the examples in a single file will prove much more practical than having a single file for each example.
* Each row is a list of binary values: `#` or `.`.
* Each position must be addressed directly with a simple way of computing coordinates.

> :warning: **Warning**:
> 
> Following part using `dict` objects was replaced with a more efficient implementation relying on `sets`.
> This part is kept as reference.

The last arguments strongly makes the case of relying on a [`dict`][py-dict] object for storing an asteroid at a given location defined by a [`tuple`][py-tuple].

```python
>>> asteroids = {(8, 4): True}
>>> asteroids.get((8, 4), False)
True
>>> asteroids.get((8, 5), False)
False
```

Converting cells into items stored into `dict` items is also straight-forward.

```python
asteroids = dict()
for row in lines:
    if len(row) > (os.linesep()):
        for cell in row:
            asteroid = cell == '#'
            if asteroid:
                asteroids[(cell, row)] = True
    else:
        yield asteroids.copy()
        asteroids = dict()
```

This leaves us with the following `load_contents()` method.

```python
def load_contents(filename: str) -> Iterator[map]:
    lines = open(filename).read().strip().split(os.linesep)
    map_ = dict()
    x: int = 0
    for line in lines:
        if len(line):
            for y, char in enumerate(line):
                if char == '.':
                    continue
                position = (x, y)
                map_[position] = char
            x += 1
        else:
            yield map_
            map_ = dict()
            x = 0
```

> :memo: **Note**:
> 
> Following is a better implementation making use of [`sets`][py-set].

```python
def load_contents(filename: str) -> Iterator[set]:
    lines = open(filename).read().strip().split(os.linesep)
    positions = set()
    y = 0
    for line in lines:
        if not len(line):
            log.debug(f'{filename=}, map of {len(positions)} items')
            yield positions
            positions = set()
            y = 0
            continue
        positions.update({(x, y) for x, c in enumerate(line) if c == '#'})
        y += 1
    yield positions
```

## 💡🙋 Puzzle Solver

First thing is:

* iterate for each asteroid, 
    * list remaining asteroids
    * iterate for each remaining asteroid
        * compute its positional offset with regard to the reference asteroid

```python
for asteroid in contents:
    others = contents - {asteroid}
    others = {tuple(a - b for a, b in zip(asteroid, o)) for o in others}
```

At its core, this puzzle consists in computing an angle for all these asteroids with regard to the reference asteroid. Solving this puzzle requires filtering asteroids keeping only one per angle, we can already guess that rounding errors will be an issue.

Thankfully the [`fractions`][py-fractions] module provides support for rational number arithmetic.

```python
>>> Fraction(4, -6)
Fraction(-2, 3)
```

This operation coupled with a reduction implemented by keeping only unique fractions values is encapsulated in a `count_asteroids()` method.

```python
def count_asteroids(rel_positions: set) -> int:
    ...
```

Obviously `Fraction` objects cannot take a denominator with a zero value, meaning that this case must be handled separately. Same thing with position symetrical with respect to the origin: we do not want to reduce positions `(2, 2)` and `(-2, -2)`. A simple way consists in separating upper and lower half with reference to the horizontal axis.

This gives us the following method:

```python
def count_asteroids(rel_positions: set) -> int:
    horizontal_asteroids = set()
    upper_asteroids = set()
    lower_asteroids = set()
    for pos in rel_positions:
        zero_denominator = pos[1] == 0
        if zero_denominator:
            horizontal_asteroids.add(
                fractions.Fraction(pos[0], abs(pos[0])).as_integer_ratio())
            continue
        upper = pos[1] > 0
        if upper:
            upper_asteroids.add(
                fractions.Fraction(pos[0], pos[1]).as_integer_ratio())
            continue
        lower = pos[1] < 0
        if lower:
            lower_asteroids.add(
                fractions.Fraction(pos[0], pos[1]).as_integer_ratio())
            continue
    asteroids = len(horizontal_asteroids) \ 
                + len(upper_asteroids) + len(lower_asteroids)
    return asteroids
```

The complete `solve()` method for part one:

```python
def solve(contents: set) -> int:
    detected_asteroids_map = dict()
    for asteroid in contents:
        others = contents - {asteroid}
        others = {tuple(a - b for a, b in zip(asteroid, o)) for o in others}
        detected_asteroids_map[asteroid] = count_asteroids(rel_positions=others)
    answer = max(detected_asteroids_map.values())
    return answer
```

Contents | Answer
--- | ---
[`examples.txt`](./examples.txt) | `[8, 33, 35, 41, 210]`
[`input.txt`](./input.txt) | `296`

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

> Once you give them the coordinates, the Elves quickly deploy an Instant Monitoring Station to the location and discover the worst: there are simply too many asteroids.
> 
> The only solution is complete vaporization by giant laser.

Nice! Would've preferred a rail gun though.

> Fortunately, in addition to an asteroid scanner, the new monitoring station also comes equipped with a giant rotating laser perfect for vaporizing asteroids. The laser starts by pointing up and always rotates clockwise, vaporizing any asteroid it hits.

The term `always rotates clockwise` is filed under *oddly specific*. 

> If multiple asteroids are exactly in line with the station, the laser only has enough power to vaporize one of them before continuing its rotation. In other words, the same asteroids that can be detected can be vaporized, but if vaporizing one asteroid makes another one detectable, the newly-detected asteroid won't be vaporized until the laser has returned to the same position by rotating a full 360 degrees.


Nice to be able of reusing all the implementation designed in part one. 

> For example, consider the following map, where the asteroid with the new monitoring station (and laser) is marked X:
> 
> ```
> .#....#####...#..
> ##...##.#####..##
> ##...#...#.#####.
> ..#.....X...###..
> ..#.#.....#....##
> ```

This example differs from those in part one.

> The first nine asteroids to get vaporized, in order, would be:
> 
> ```
> .#....###24...#..
> ##...##.13#67..9#
> ##...#...5.8####.
> ..#.....X...###..
> ..#.#.....#....##
> ```
> 
> Note that some asteroids (the ones behind the asteroids marked 1, 5, and 7) won't have a chance to be vaporized until the next full rotation. The laser continues rotating; the next nine to be vaporized are:
> 
> ```
> .#....###.....#..
> ##...##...#.....#
> ##...#......1234.
> ..#.....X...5##..
> ..#.9.....8....76
> ```
> 
> The next nine to be vaporized are then:
> 
> ```
> .8....###.....#..
> 56...9#...#.....#
> 34...7...........
> ..2.....X....##..
> ..1..............
> ```
> 
> Finally, the laser completes its first full rotation (1 through 3), a second rotation (4 through 8), and vaporizes the last asteroid (9) partway through its third rotation:
> 
> ```
> ......234.....6..
> ......1...5.....7
> .................
> ........X....89..
> .................
> ```
> 
> In the large example above (the one with the best monitoring station location at 11,13):
> 
> ```
> The 1st asteroid to be vaporized is at 11,12.
> The 2nd asteroid to be vaporized is at 12,1.
> The 3rd asteroid to be vaporized is at 12,2.
> The 10th asteroid to be vaporized is at 12,8.
> The 20th asteroid to be vaporized is at 16,0.
> The 50th asteroid to be vaporized is at 16,9.
> The 100th asteroid to be vaporized is at 10,16.
> The 199th asteroid to be vaporized is at 9,6.
> The 200th asteroid to be vaporized is at 8,2.
> The 201st asteroid to be vaporized is at 10,9.
> The 299th and final asteroid to be vaporized is at 11,1.
> ```

Thankfully we have quite a lot of details which greatly help for QA.

> The Elves are placing bets on which will be the 200th asteroid to be vaporized. Win the bet by determining which asteroid that will be; what do you get if you multiply its X coordinate by 100 and then add its Y coordinate? (For example, 8,2 becomes 802.)

## 🤔🤯 Puzzle Solver

The puzzle instructions state that a clockwise scanning operation is performed, meaning that the angle is always increasing. Further it indicated that if multiple asteroids are on a given angle, only the closest one will be blasted. This leaves us with the following algorithm:

* Map the number of detected asteroids from each asteroid position
* Find the position of the station which yields the highest number of detected asteroids
* Compute angles and distance of all the other asteroids
* Remove N asteroids each time moving the angle clockwise
* Compute the answer based on the position of the Nth removed asteroid  

```python
def solve_part_two(contents: map) -> int:
    detected_asteroids_map = map_detected_asteroids(asteroids=contents)
    max_asteroids = max(detected_asteroids_map.values())
    index = list(detected_asteroids_map.values()).index(max_asteroids)
    station = list(detected_asteroids_map.keys())[index]
    asteroids = contents - {station}
    polar_positions = compute_positions(reference=station, asteroids=asteroids)
    polar_map = map_polar_positons(polar_positions=polar_positions)
```

Rather than duplicating the logic present in the part one `solve()` method, I went on factorizing it in a `map_detected_asteroids()` method.

```python
def map_detected_asteroids(asteroids: set) -> map:
    detected_asteroids_map = dict()
    for asteroid in asteroids:
        others = asteroids - {asteroid}
        polar_positions = compute_positions(reference=asteroid,
                                            asteroids=others)
        angles = set(p[1] for p in polar_positions)
        detected_asteroids_map[asteroid] = len(angles)
    return detected_asteroids_map
```

The mapping logic was improved using a [polar coordinates][w-polar] transform instead of relying on fractions and byzantine comparison logic. The [`cmath`][py-cmath] module provides all the required methods for this operation.

```python
def compute_positions(reference: tuple, asteroids: set[tuple]) -> set:
    positions = set()
    rel_positions = compute_offsets(reference=reference, asteroids=asteroids)
    for pos in rel_positions:
        distance, angle = cmath.polar(complex(*pos))
        positions.add((distance, angle))
    return positions
```

The runtime of part one is significantly lowered.

```python
cmath.polar(complex(1, 4))
(4.123105625617661, 1.3258176636680326)
cmath.polar(complex(2, 8))
(8.246211251235321, 1.3258176636680326)
```



Contents | Answer
--- | ---

# 🚀✨ Further Improvements

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-10]: https://adventofcode.com/2019/day/10

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
