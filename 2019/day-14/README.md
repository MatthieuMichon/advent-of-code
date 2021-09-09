Solution in [Python][py] for the [day 14 puzzle][aoc-2019-14] of the [2019 edition][aoc-2019] of the [Advent of Code][aoc] annual programming challenge.

# 🎄🌟🌟 Space Stoichiometry 🎄🌟🌟

## 🔍📖 Annotated Puzzle Statement

> As you approach the rings of Saturn, your ship's low fuel indicator turns on. There isn't any fuel here, but the rings have plenty of raw material. Perhaps your ship's Inter-Stellar Refinery Union brand nanofactory can turn these raw materials into fuel.
> 
> You ask the nanofactory to produce a list of the reactions it can perform that are relevant to this process (your puzzle input).

The *puzzle input* is a **list** of *reactions*.

> Every reaction turns some quantities of specific input chemicals into some quantity of an output chemical.

A *reaction* associates a *number* of **quantified input chemicals** with a **quantity of output chemical**.

> Almost every chemical is produced by exactly one reaction; the only exception, `ORE`, is the raw material input to the entire process and is not produced by a reaction.

We should never have an equation where the `ORE` chemical is on the right-hand side (RHS) of the equation.

> You just need to know how much `ORE` you'll need to collect before you can produce one unit of `FUEL`.

The implied algorithm starts with a unitary amount of the final chemical `FUEL`, and makes it way back to elementary `ORE` chemicals.

> Each reaction gives specific quantities for its inputs and output; reactions cannot be partially run, so only whole integer multiples of these quantities can be used. (It's okay to have leftover chemicals when you're done, though.)

Rather then computing decimal quantities, arithmetics results should be rounded up to the nearest larger integer value.

> 
> For example, the reaction:
> ```
> 1 A, 2 B, 3 C => 2 D
> ```
> means that exactly `2` units of chemical `D` can be produced by consuming exactly `1 A`, `2 B` and `3 C`. You can run the full reaction as many times as necessary; for example, you could produce `10 D` by consuming `5 A`, `10 B`, and `15 C`.
> 
> Suppose your nanofactory produces the following list of reactions:
> ```
> 10 ORE => 10 A
> 1 ORE => 1 B
> 7 A, 1 B => 1 C
> 7 A, 1 C => 1 D
> 7 A, 1 D => 1 E
> 7 A, 1 E => 1 FUEL
> ```

Parsing the input contents should also be easy.

> The first two reactions use only ORE as inputs; they indicate that you can produce as much of chemical A as you want (in increments of 10 units, each 10 costing 10 ORE) and as much of chemical B as you want (each costing 1 ORE). To produce 1 FUEL, a total of 31 ORE is required: 1 ORE to produce 1 B, then 30 more ORE to produce the 7 + 7 + 7 + 7 = 28 A (with 2 extra A wasted) required in the reactions to convert the B into C, C into D, D into E, and finally E into FUEL. (30 A is produced because its reaction requires that it is created in increments of 10.)

No comments.

> Or, suppose you have the following list of reactions:
> ```
> 9 ORE => 2 A
> 8 ORE => 3 B
> 7 ORE => 5 C
> 3 A, 4 B => 1 AB
> 5 B, 7 C => 1 BC
> 4 C, 1 A => 1 CA
> 2 AB, 3 BC, 4 CA => 1 FUEL
> ```

Reading these previous lines, a tokenization process could be implemented in the following steps:

1. Splitting the line into two parts using the string '` => `' as a separator.
1. Splitting the left-end side using the string '`, `'.
1. For each of the tokens split across the space character and convert the left side into an integer.
1. Final arrangement and conversion to key / value.

Step | Items
--- | ---
0 | `'2 AB, 3 BC, 4 CA => 1 FUEL'`
1 | `('2 AB, 3 BC, 4 CA', '1 FUEL')`
2 | `(('2 AB', '3 BC', '4 CA'), '1 FUEL')`
3 | `(((2, 'AB'), (3, 'BC'), (4, 'CA')), (1, 'FUEL'))`
4 | `'FUEL': ('AB': 2, 'BC': 3, 'CA': 4)`

> The above list of reactions requires 165 ORE to produce 1 FUEL:
> ```
> Consume 45 ORE to produce 10 A.
> Consume 64 ORE to produce 24 B.
> Consume 56 ORE to produce 40 C.
> Consume 6 A, 8 B to produce 2 AB.
> Consume 15 B, 21 C to produce 3 BC.
> Consume 16 C, 4 A to produce 4 CA.
> Consume 2 AB, 3 BC, 4 CA to produce 1 FUEL.
> ```
> Here are some larger examples:
> 
> 13312 ORE for 1 FUEL:
> ```
> 157 ORE => 5 NZVS
> 165 ORE => 6 DCFZ
> 44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
> 12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
> 179 ORE => 7 PSHF
> 177 ORE => 5 HKGWZ
> 7 DCFZ, 7 PSHF => 2 XJWVT
> 165 ORE => 2 GPVTF
> 3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
> ```
> 180697 ORE for 1 FUEL:
> ```
> 2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
> 17 NVRVD, 3 JNWZP => 8 VPVL
> 53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
> 22 VJHF, 37 MNCFX => 5 FWMGM
> 139 ORE => 4 NVRVD
> 144 ORE => 7 JNWZP
> 5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
> 5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
> 145 ORE => 6 MNCFX
> 1 NVRVD => 8 CXFTF
> 1 VJHF, 6 MNCFX => 4 RFSQX
> 176 ORE => 6 VJHF
> ```
> 2210736 ORE for 1 FUEL:
> ```
> 171 ORE => 8 CNZTR
> 7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
> 114 ORE => 4 BHXH
> 14 VRPVC => 6 BMBT
> 6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
> 6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
> 15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
> 13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
> 5 BMBT => 4 WPTQ
> 189 ORE => 9 KTJDG
> 1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
> 12 VRPVC, 27 CNZTR => 2 XDBXC
> 15 KTJDG, 12 BHXH => 5 XCVML
> 3 BHXH, 2 VRPVC => 7 MZWV
> 121 ORE => 7 VRPVC
> 7 XCVML => 6 RJRHP
> 5 BHXH, 4 VRPVC => 5 LTCX
> ```
> Given the list of reactions in your puzzle input, what is the minimum amount of ORE required to produce exactly 1 FUEL?

## 💾🔍 Content Decoding

The puzzle input was described as a list of objects, meaning that the decoder method body will start by breaking down the input file into lines.

```python
lines = open(file).read().strip().split(os.linesep)
assert all(_EQ_OPERATOR in l for l in lines)
log.info(f'Loaded {len(lines)} lines from {file=}')
```

Thankfully the `assert` check passes.

```shell
# 303 - load_contents    - INFO     - Loaded 59 lines from file=PosixPath('input.txt')
```

Next thing is to iterate over each line and process both sides.

```python
for l in lines:
    lhs, rhs = l.split(_EQ_OPERATOR)
    lhs = tuple(split_lhs(lhs))
    rhs_qty, rhs_name = tuple(split_chem(rhs))
```

Two nested methods `split_lhs()` and `split_chem()` are used for low-level string manipulation.

```python
def split_lhs(lhs: str) -> Iterator:
    chems = lhs.split(_LHS_SEPARATOR)
    for chem in chems:
        yield split_chem(chem)

def split_chem(chem: str) -> (int, str):
    qty, name = chem.split(_CHEM_SEPARATOR)
    qty = int(qty)
    return qty, name
```

The complete `load_contents()` method in all its glory:

```python
def load_contents(file: Path) -> Iterator:
    """Load and convert contents from a filename

    :param file: input file handle
    :return: iterator yielding a dict entry for each chemical reaction
    """
    _EQ_OPERATOR = ' => '
    _LHS_SEPARATOR = ', '
    _CHEM_SEPARATOR = ' '

    def split_lhs(lhs: str) -> Iterator:
        chems = lhs.split(_LHS_SEPARATOR)
        for chem in chems:
            yield split_chem(chem)

    def split_chem(chem: str) -> (int, str):
        qty, name = chem.split(_CHEM_SEPARATOR)
        qty = int(qty)
        return qty, name

    lines = open(file).read().strip().split(os.linesep)
    assert all(_EQ_OPERATOR in l for l in lines)
    log.info(f'Loaded {len(lines)} lines from {file=}')
    for l in lines:
        lhs, rhs = l.split(_EQ_OPERATOR)
        lhs = tuple(split_lhs(lhs))
        rhs_qty, rhs_name = tuple(split_chem(rhs))
        yield rhs_name, {'qty': rhs_qty, 'lhs': lhs}
```

```shell
# 642 - main             - DEBUG    - Arguments: Namespace(filename='input.txt', part=1, verbose=True)
# 642 - load_contents    - INFO     - Loaded 59 lines from file=PosixPath('input.txt')
{'DQFL': {'qty': 9, 'lhs': ((180, 'ORE'),)}, 'ZBLC': {'qty': 8, 'lhs': ((3, 'HGCR'), (9, 'TKRT'))}, ...
```

## 💡🙋 Implementation

Struggled a bit on this puzzle. First intuition was to use a depth-first search with a recursive function. This however didn't work out due to the need of handling lots and left-overs.

The computation method required to be replaced by a [breath-first search][w-bfs] which yielded the correct results.

```python
def do_bfs(chem_map: dict) -> int:
    """Execute a breadth-first search

    :param chem_map: chemical reactions map
    :return: answer
    """
    reactions = list()
    reactions.append({'chem': 'FUEL', 'qty': 1})
    req_qty = defaultdict(int)
    ore_qty = 0
    while len(reactions):
        reaction = reactions.pop()
        chem_name = reaction['chem']
        if chem_name == 'ORE':
            ore_qty += reaction['qty']
        elif reaction['qty'] <= req_qty[chem_name]:
            req_qty[chem_name] -= reaction['qty']
        else:
            qty_required = reaction['qty'] - req_qty[chem_name]
            new_reaction = chem_map[chem_name]
            lots = math.ceil(qty_required / new_reaction['lot'])
            for lhs_chem in new_reaction['chems']:
                reactions.append({'chem': lhs_chem[1], 'qty': lots * lhs_chem[0]})
            qty_extra = lots * new_reaction['lot'] - qty_required
            req_qty[chem_name] = qty_extra
    return ore_qty
```

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-14.py input.txt -p 1` | `399063`

# 😰🙅 Part Two

## 🥺👉👈 Annotated Statement

> After collecting `ORE` for a while, you check your cargo hold: **1 trillion** (1000000000000) units of `ORE`.

Thankfully Python is not limited to mere 32-bit integers.

> With that much ore, given the examples above:
> ```
> The 13312 ORE-per-FUEL example could produce 82892753 FUEL.
> The 180697 ORE-per-FUEL example could produce 5586022 FUEL.
> The 2210736 ORE-per-FUEL example could produce 460664 FUEL.
> ```
> 
> Given 1 trillion ORE, what is the maximum amount of FUEL you can produce?

Intuitively we could get away by just using a [binary search][w-binary-search] on the results and closing in on the final value.

## 🤔🤯 Puzzle Solver

First thing is to pass the target `FUEL` quantity value:

```python
def do_bfs(chem_map: dict, fuel_qty: int = 1) -> int:
    """Execute a breadth-first search

    :param chem_map: chemical reactions map
    :param fuel_qty: number of FUEL units to produce
    :return: answer
    """
    reactions = list()
    reactions.append({'chem': 'FUEL', 'qty': fuel_qty})
```

Next was implementing the binary search, with the start point computed by using a cross-multiplication. Knowing the ratio of `ORE` requird for producing a single unit of `FUEL`, we can compute the lower boundary of the quantity `FUEL` produced by one trillion amount of `ORE`. Again the final value will be higher due to left-overs being used for other chemical reactions.

```python
target_ore_quantity = 1000000000000
fuel_qty = 1
required_ore = do_bfs(chem_map=reactions, fuel_qty=fuel_qty)
lower_fuel_qty = target_ore_quantity // required_ore
```

Next step is computing the upper boundary, here nothing fancy we simply multiply by 10 %:

```python
upper_fuel_qty = int(1.1 * lower_fuel_qty)
while target_ore_quantity > do_bfs(chem_map=reactions, fuel_qty=upper_fuel_qty):
    upper_fuel_qty = int(1.1 * upper_fuel_qty)
```

Finally the binary search is performed by computing the half point, and depending if it yields below or above the target ore quantity either the lower or upper bound is updated. The exit condition being when both bounds are separated by a single unit.

```python
while upper_fuel_qty - lower_fuel_qty > 1:
    bissect_fuel_qty = (lower_fuel_qty + upper_fuel_qty) // 2
    log.debug(f'Computed {bissect_fuel_qty=}')
    required_ore = do_bfs(chem_map=reactions, fuel_qty=bissect_fuel_qty)
    more_fuel = required_ore < target_ore_quantity
    if more_fuel:
        lower_fuel_qty = bissect_fuel_qty
    else:
        upper_fuel_qty = bissect_fuel_qty
```

The complete method:

```python
def solve_part_two(reactions: dict) -> int:
    """Provide answer for part one of the puzzle

    :param reactions: mapping of chemical reactions
    :return: answer of part one
    """

    target_ore_quantity = 1000000000000
    fuel_qty = 1
    required_ore = do_bfs(chem_map=reactions, fuel_qty=fuel_qty)
    lower_fuel_qty = target_ore_quantity // required_ore
    log.info(f'Computed {lower_fuel_qty=}')
    upper_fuel_qty = int(1.1 * lower_fuel_qty)
    while target_ore_quantity > do_bfs(chem_map=reactions, fuel_qty=upper_fuel_qty):
        upper_fuel_qty = int(1.1 * upper_fuel_qty)
    log.info(f'Computed {upper_fuel_qty=}')

    while upper_fuel_qty - lower_fuel_qty > 1:
        bissect_fuel_qty = (lower_fuel_qty + upper_fuel_qty) // 2
        log.debug(f'Computed {bissect_fuel_qty=}')
        required_ore = do_bfs(chem_map=reactions, fuel_qty=bissect_fuel_qty)
        more_fuel = required_ore < target_ore_quantity
        if more_fuel:
            lower_fuel_qty = bissect_fuel_qty
        else:
            upper_fuel_qty = bissect_fuel_qty
    answer = lower_fuel_qty
    return answer
```

Contents | Command | Answer
--- | --- | ---
[`input.txt`](./input.txt) | `./day-14.py input.txt -p 2` | `4215654`

# 🙄😔 Closing Thoughts

Part one contained a technicality requiring a breadth-first_search, which wasn't caught upon first reading and required some  additional logic for tracking required vs produced chemical quantities. On the other hand part two was straightforward.

[aoc]: https://adventofcode.com/
[aoc-2019]: https://adventofcode.com/2019/
[aoc-intro]: https://adventofcode.com/2019/about
[aoc-2019-9]: https://adventofcode.com/2019/day/9
[aoc-2019-14]: https://adventofcode.com/2019/day/14

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

[w-binary-search]: https://en.wikipedia.org/wiki/Binary_search_algorithm
[w-cartesian]: https://en.wikipedia.org/wiki/Polar_coordinate_system
[w-polar]: https://en.wikipedia.org/wiki/Polar_coordinate_system
[w-bfs]: https://en.wikipedia.org/wiki/Breadth-first_search
