Solution in [Python][py] for the [day 12 puzzle][aoc-2019-12] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 The N-Body Problem 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> The space near Jupiter is not a very safe place; you need to be careful of a big distracting red spot, extreme radiation, and a whole lot of moons swirling around. You decide to start by tracking the four largest moons: Io, Europa, Ganymede, and Callisto.
> 
> After a brief scan, you calculate the position of each moon (your puzzle input). You just need to simulate their motion so you can avoid them.

Dreadful choice of words: *Just need to simulate*, particularly with N-body.

> Each moon has a 3-dimensional position (x, y, and z) and a 3-dimensional velocity. The position of each moon is given in your scan; the x, y, and z velocity of each moon starts at 0.

Matrix calculation intensifies.

> Simulate the motion of the moons in time steps.

Good news!

> Within each time step, first update the velocity of every moon by applying gravity. Then, once all moons' velocities have been updated, update the position of every moon by applying velocity. Time progresses by one step once all of the positions are updated.
>
> To apply gravity, consider every pair of moons. On each axis (x, y, and z), the velocity of each moon changes by exactly +1 or -1 to pull the moons together. For example, if Ganymede has an x position of 3, and Callisto has a x position of 5, then Ganymede's x velocity changes by +1 (because 5 > 3) and Callisto's x velocity changes by -1 (because 3 < 5). However, if the positions on a given axis are the same, the velocity on that axis does not change for that pair of moons.

For each of the bodies, each of its axis must be compared with each of the other axis. This translates in `3 x N x (N - 1)` comparisons, an operation with a quadratic time complexity.

> Once all gravity has been applied, apply velocity: simply add the velocity of each moon to its own position. For example, if Europa has a position of x=1, y=2, z=3 and a velocity of x=-2, y=0, z=3, then its new position would be x=-1, y=2, z=6. This process does not modify the velocity of any moon.

Computing velocity never was so easy!

> For example, suppose your scan reveals the following positions:
> ```
> <x=-1, y=0, z=2>
> <x=2, y=-10, z=-7>
> <x=4, y=-8, z=8>
> <x=3, y=5, z=-1>
> ```
> 
> Simulating the motion of these moons would produce the following:
> 
> After 0 steps:
> ```
> pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
> pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
> pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
> pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>
> ```
> 
> After 1 step:
> ```
> pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
> pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
> pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
> pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>
> ```
> 
> After 10 steps:
> ```
> pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
> pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
> pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
> pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>
> ```

No surprises.

> Then, it might help to calculate the total energy in the system. The total energy for a single moon is its potential energy multiplied by its kinetic energy.

I recall an addition rather than a multiplication, what an interesting universe!

> A moon's potential energy is the sum of the absolute values of its x, y, and z position coordinates. A moon's kinetic energy is the sum of the absolute values of its velocity coordinates. Below, each line shows the calculations for a moon's potential energy (pot), kinetic energy (kin), and total energy:
> 
> Energy after 10 steps:
> ```
> pot: 2 + 1 + 3 =  6;   kin: 3 + 2 + 1 = 6;   total:  6 * 6 = 36
> pot: 1 + 8 + 0 =  9;   kin: 1 + 1 + 3 = 5;   total:  9 * 5 = 45
> pot: 3 + 6 + 1 = 10;   kin: 3 + 2 + 3 = 8;   total: 10 * 8 = 80
> pot: 2 + 0 + 4 =  6;   kin: 1 + 1 + 1 = 3;   total:  6 * 3 = 18
> Sum of total energy: 36 + 45 + 80 + 18 = 179
> ```
> 
> In the above example, adding together the total energy for all moons after 10 steps produces the total energy in the system, 179.

No surprises here neither.

> Here's a second example:
> ```
> <x=-8, y=-10, z=0>
> <x=5, y=5, z=10>
> <x=2, y=-7, z=3>
> <x=9, y=-8, z=-3>
> ```
> 
> Every ten steps of simulation for 100 steps produces:
> 
> After 0 steps:
> ```
> pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
> pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>
> pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>
> pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>
> ```
> 
> After 10 steps:
> ```
> pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>
> pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>
> pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>
> pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>
> ```
> 
> After 100 steps:
> ```
> pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
> pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
> pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
> pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>
> ```
> 
> Energy after 100 steps:
> ```
> pot:  8 + 12 +  9 = 29;   kin: 7 +  3 + 0 = 10;   total: 29 * 10 = 290
> pot: 13 + 16 +  3 = 32;   kin: 3 + 11 + 5 = 19;   total: 32 * 19 = 608
> pot: 29 + 11 +  1 = 41;   kin: 3 +  7 + 4 = 14;   total: 41 * 14 = 574
> pot: 16 + 13 + 23 = 52;   kin: 7 +  1 + 1 =  9;   total: 52 *  9 = 468
> Sum of total energy: 290 + 608 + 574 + 468 = 1940
> ```

Understood.

> What is the total energy in the system after simulating the moons given in your scan for 1000 steps?

Due to quadratic time complexity, a thousand steps could require a substantial amount of computations with a double-digit body count.

## 💡🙋 Implementation

First thing is having a look in the input supplied for this puzzle. This will provide answers to question regarding the number of bodies.

For instance, we have:

```
<x=7, y=10, z=17>
<x=-2, y=7, z=0>
<x=12, y=5, z=12>
<x=5, y=-8, z=6>
```

> :memo: Note:
> 
> With four bodies the number of computations is not a concern.

There are several ways to decode contents:

* As a [`list`][py-list]: `[7, 10, 17]`
* As a [`dict`][py-dict]: `{'x': 7, 'y': 10, 'z': 17}`

As we never know what part two has in store, we will use a map.

```python
def load_contents(filename: str) -> Iterator[map]:
    lines = open(filename).read().strip().strip('<>').split(os.linesep)
    for line in lines:
        axis = [token.split('=') for token in line.strip('<>').split(',')]
        axis = {name: int(value) for name, value in axis}
        yield axis
```

## 💡 Solver

The algorithm for part one is quite simple:

* initialize velocity vectors
* for each time step
    * for each moon pair permutation
        * for each axis
            * compare position values and update the velocity value
    * for each body
        * for each axis
            * update position using the velocity of relevant body and axis
* compute the total energy    

With the corresponding source code:

```python
def solve(contents: list[map], steps: int) -> int:
    positions = contents
    velocities = [{axis: 0 for axis in body.keys()} for body in positions]
    for step in range(steps):
        if not step % 10:
            trace(step, positions, velocities)
        compute_time_step(positions, velocities)
    total_energy = compute_total_energy(positions, velocities)
    return total_energy
```

The `compute_time_step()` uses reference passing for updating the values without having to return anything. Permutations are computed using [`itertools.permutations`][py-itertools-permutations].

```python
def compute_time_step(positions: list[map], velocities: list[map]) -> None:
    bodies = range(len(positions))
    for ref, opp in permutations(bodies, 2):
        ref_pos = positions[ref]
        opp_pos = positions[opp]
        for axis, ref_val in ref_pos.items():
            if ref_val < opp_pos[axis]:
                velocities[ref][axis] += 1
            elif ref_val > opp_pos[axis]:
                velocities[ref][axis] -= 1
    for body, pos in enumerate(positions):
        for axis in pos.keys():
            pos[axis] += velocities[body][axis]
```

The `compute_total_energy()` is also quite trivial:

```python
def compute_total_energy(positions: list[map], velocities: list[map]) -> int:
    total_energy = 0
    for body, pos in enumerate(positions):
        body_energy = sum(map(abs, pos.values()))
        kin = velocities[body]
        body_energy *= sum(map(abs, kin.values()))
        total_energy += body_energy
    return total_energy
```

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-12.py input.txt -p 1` | `9958`

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

> All this drifting around in space makes you wonder about the nature of the universe. Does history really repeat itself? You're curious whether the moons will ever return to a previous state.
> 
> Determine the number of steps that must occur before all of the moons' positions and velocities exactly match a previous point in time.

Feels like an optimization problem.

> For example, the first example above takes 2772 steps before they exactly match a previous point in time; it eventually returns to the initial state:
> ```
> After 0 steps:
> pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
> pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
> pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
> pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>
> 
> After 2770 steps:
> pos=<x=  2, y= -1, z=  1>, vel=<x= -3, y=  2, z=  2>
> pos=<x=  3, y= -7, z= -4>, vel=<x=  2, y= -5, z= -6>
> pos=<x=  1, y= -7, z=  5>, vel=<x=  0, y= -3, z=  6>
> pos=<x=  2, y=  2, z=  0>, vel=<x=  1, y=  6, z= -2>
> 
> After 2771 steps:
> pos=<x= -1, y=  0, z=  2>, vel=<x= -3, y=  1, z=  1>
> pos=<x=  2, y=-10, z= -7>, vel=<x= -1, y= -3, z= -3>
> pos=<x=  4, y= -8, z=  8>, vel=<x=  3, y= -1, z=  3>
> pos=<x=  3, y=  5, z= -1>, vel=<x=  1, y=  3, z= -1>
> 
> After 2772 steps:
> pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
> pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
> pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
> pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>
> ```

Interestingly velocities are zero for all the bodies and axis.

> Of course, the universe might last for a very long time before repeating. Here's a copy of the second example from above:
> ```
> <x=-8, y=-10, z=0>
> <x=5, y=5, z=10>
> <x=2, y=-7, z=3>
> <x=9, y=-8, z=-3>
> ```

Corresponding velocities are also zero. Coincidence? 🤔 I think not!

> This set of initial positions takes `4686774924` steps before it repeats a previous state! Clearly, you might need to find a more efficient way to simulate the universe.

4M steps mean that any sort of correlation can be forgotten.

> How many steps does it take to reach the first state that exactly matches a previous state?

## 🤔🤯 Puzzle Solver

Instead of looping on each body, a more efficient way is to loop on each axis.

```python
pos_per_axis = [[body[axis] for body in contents] for axis in contents[0].keys()]
vel_per_axis = [[0 for _ in contents] for axis in contents[0].keys()]
```

```python
def step_by_axis(
        positions: list[list[int]], velocities: list[list[int]]) -> None:
    for axis, bodies in enumerate(positions):
        for bindex, body in enumerate(bodies):
            velocities[axis][bindex] += \
                sum(opp > body for opp in bodies) - \
                sum(body > opp for opp in bodies)
        for bindex, body in enumerate(bodies):
            bodies[bindex] += velocities[axis][bindex]
```

Performance is much better, however still too slow for computing the value in less than a few dozen seconds.

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-12.py input.txt -p 2` | ``

# 🚀✨ Further Improvements

The `print_panels()` could be improved.

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-12]: https://adventofcode.com/2019/day/12

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
