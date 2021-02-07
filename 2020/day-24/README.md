# Day 24: Lobby Layout

## Summary

Puzzle | Decoding | Transform | Iterations | Epilogue
--- | --- | --- | --- | ---
Day 24 Part One | [`file -> list[list[int]]`](#input-decoding) | [Optimization](#initial-transform) | tbd | tbd

## Initial Thoughts

> A member of the renovation crew gives you a list of the tiles that need to be flipped over (your puzzle input).

>  Each line in the list identifies a single tile that needs to be flipped by giving a series of steps starting from a reference tile in the very center of the room.

The puzzle input consists in a file containing a number of lines. Each line is a **path**, a series of **steps** starting from the center of the room leading to a **tile** needing to be flipped.

> Because the tiles are hexagonal, every tile has six neighbors: east, southeast, southwest, west, northwest, and northeast. These directions are given in your list, respectively, as e, se, sw, w, nw, and ne.

Each step consists in moving in one of six directions for a single unit of length. A simple idea consists in translating these directions in angular moves:

Step | Heading
--- | ---
`ne` | 30 
`e` | 90 
`se` | 150 
`sw` | 210 
`w` | 270 
`nw` | 330 

The lack of delimitation between the steps constitutes a small hurdle due to the *ambiguity* of how these directions are encoded.

Steps | Sequence
--- | ---
`eee` | `e`; `e`; `e`
`neesee` | `ne`; `e`; `se`; `e`

> Tiles might be flipped more than once.

> After all of the instructions have been followed, how many tiles are left with the black side up?

Not surprisingly, several different paths may lead the same tile. The opposite would mean that simply counting the lines would be yield the answer.

## Puzzle Part One

### Input Decoding

Input contents have the following characteristics:

* Text file
* A number of lines, with each line being a path consisting in a sequence of steps
* Each step being one the six values detailed in the table above

A quick and dirty way for decoding these steps while avoiding ambiguity would consist in three passes. The trick consists in arranging the ordering leaving the ambiguous values last.

Step | Char
--- | ---
`ne` | `1` 
`e` | `2` 
`se` | `3`
`sw` | `4` 
`w` | `5` 
`nw` | `6` 

```python
DIRECTION_MAP = {
    'ne': '1', 'se': '3', 'sw': '4', 'nw': '6',
    'e': '2', 'w': '5',
}
```

A first pass for replacing occurrences of two-lettered steps by single digits. A second pass for replacing the remaining single-lettered steps (`e` or `w`) and finally a third and last pass for converting these values into degrees.

```python
for d, v in DIRECTION_MAP.items():
    paths = paths.replace(d, v)
```
 
The result would be a list of headings encoded as integer in degrees.

```python
paths = paths.split(os.linesep)
paths = [[-30 + (int(s) * 60) for s in p] for p in paths if len(p)]
```

This gives a first input decoding method.

```python
DIRECTION_MAP = {
    'ne': '1', 'se': '3', 'sw': '4', 'nw': '6',
    'e': '2', 'w': '4',
}


def read_paths(file: Path) -> list[list[int]]:
    paths = open(file).read()
    for d, v in DIRECTION_MAP.items():
        paths = paths.replace(d, v)
    paths = paths.split(os.linesep)
    paths = [[-30 + (int(s) * 60) for s in p] for p in paths if len(p)]
    return paths
```

Decoding example:

* Input: `seswneswswsenwwnwse`
* Output: `[150, 210, 30, 210, 210, 150, 330, 270, 330, 150]`

Quick check:

```python
>>> set(a for p in paths for a in p)
{330, 270, 210, 150, 90, 30}
```

### Initial Transform

Each path has a number of steps which when travelled lead to a destination tile. These steps are **commutative**, meaning their order does not affect the destination tile.

```python
from collections import Counter


paths = [Counter(p) for p in paths]
```

Furthermore pairs of opposite steps (with an angular difference of 180 degrees) cancel out, meaning they can be removed without affecting the destination tile.

```python
distance = path[angle] - path[180 + angle]
heading = angle if distance >= 0 else 180 + angle
optimized_steps.extend([heading] * abs(distance))
```

The complete optimization method:

```python
def optimize(paths: list[list[int]]) -> list[list[int]]:
    paths = [Counter(p) for p in paths]
    optimized_paths = list()
    for path in paths:
        optimized_steps = list()
        for angle in ANGLES:
            if angle > 180:
                break
            distance = path[angle] - path[180 + angle]
            heading = angle if distance >= 0 else 180 + angle
            optimized_steps.extend([heading] * abs(distance))
        optimized_paths.append(optimized_steps)
    return optimized_paths
```
