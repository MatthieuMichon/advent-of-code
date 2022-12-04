# 🎄🌟🌟 Smoke Basin 🎄🌟🌟

## 💾 Content Decoding

This challenge requires performing computations on a two-dimensional array, such as comparing values with neighboring cells.

The input contents is laid a bitmap, with each char defining a height of a given cell. Decoding these contents thus involves iterating over rows followed by columns. Rather than directly assigning the height, I choose to create a single entry map for makingn subsequent addition of per-cell metadata easier. 

```python
def load_contents(filename: Path) -> Generator:
    """Load and convert contents from file

    :param filename: input filename
    :return: map generator
    """
    with open(filename, encoding='utf-8') as buffer:
        for row, line in enumerate(buffer.readlines()):
            for col, cell in enumerate(line.strip()):
                yield (col, row), {'height': int(cell)}
```

## 💡 First Part

> Your first goal is to find the low points - the locations that are lower than any of its adjacent locations.

This first part calls for two methods: one testing if a given position is at a low point which we shall call `test_low_point()` and a second one for computing the neighbors `compute_neighbors()`.

I decided to go with a solution able to handle more than two axis, for anticipating challenges involving a three-dimensional space).

```python
from itertools import product

AXIS = 2
STENCILS = tuple(product((-1, 0, 1), repeat=AXIS))
```

This produces the following combination:

```
((-1, -1), (-1, 0), (-1, 1),
(0, -1), (0, 0), (0, 1),
(1, -1), (1, 0), (1, 1))
```

For this challenge diagonals must be disregarded, also the present position `(0, 0)` must be ignored.

```python
STENCILS_NO_DIAG = tuple(n for n in STENCILS if 0 < sum(map(abs, n)) < 2)
```

This leaves with the four following neighbors.

```
((-1, 0), (0, -1), (0, 1), (1, 0))
```

Next task is to offset the stencil with the position.

```python
def compute_neighbors(pos: tuple[int]) -> tuple:
    neighbors = tuple(tuple([sum(x) for x in zip(pos, s)]) 
                      for s in STENCILS_NO_DIAG)
    return neighbors

```

Following is comparing the height of all these neighbors:

```python
def test_low_point(contents: dict, position: tuple, size: int) -> bool:
    if position not in contents:
        return False
    neighbors = compute_neighbors(pos=position, size=size)
    low_point = all(
        n not in contents or
        contents[position]['height'] < contents[n]['height']
        for n in neighbors)
    return low_point
```

The `solve_part_one()` function computes the answer by iterating over the complete grid. 

```python
def solve_part_one(contents: dict) -> int:
    keys = contents.keys()
    rows = 1 + max(k[0] for k in keys)
    heights = (contents[pos]['height']
               for pos in keys
               if test_low_point(contents=contents, position=pos, size=rows))
    answer = sum(1 + int(h) for h in heights)
    return answer
```

| Contents                   | Command           | Answer | Time    |
|----------------------------|-------------------|--------|---------|
| [`input.txt`](./input.txt) | `./day_9.py -p 1` | `585`  | 29.6 ms | 

# 😰 Second Part

I went with a top to bottom approach, starting with the method responsible for computing the result.

```python
DEFAULT_HEIGHT = 9
DEFAULT_POS = {'height': DEFAULT_HEIGHT, 'low_point': False, 'basin': False}

def solve_part_two(contents: dict) -> int:
    keys = contents.keys()
    rows = 1 + max(k[0] for k in keys)
    heightmap = {k: dict(DEFAULT_POS, **v) for k, v in contents.items()}
    low_points = (pos for pos in keys if test_low_point(
        contents=contents, position=pos, size=rows))
    basin_sizes = list()
    for pt in low_points:
        heightmap[pt]['low_point'] = True
        basin_sizes.append(fill(pt, heightmap=heightmap, size=rows))
        basin_sizes.sort(reverse=True)
    answer = math.prod(basin_sizes[:3])
    return answer
```

The `fill()` method being a simple breath-first search method.

```python
def fill(pos, heightmap, size) -> int:
    basin_size = 0
    locations = collections.deque()
    locations.append(pos)
    while locations:
        pos = locations.popleft()
        if inside(pos=pos, heightmap=heightmap, size=size):
            heightmap[pos]['basin'] = True
            basin_size += 1
        for n in compute_neighbors(pos):
            if n in heightmap and inside(pos=n, heightmap=heightmap, size=size):
                locations.append(n)
    return basin_size
```

The `inside()` method checks if a cell belongs to a basin:

```python
def test_basin(contents: dict, position: tuple, size: int) -> bool:
    if position not in contents or contents[position]['height'] == 9:
        return False
    neighbors = compute_neighbors(pos=position)
    basin = all(
        contents[n]['low_point'] or
        contents[n]['basin'] or
        contents[position]['height'] <= contents[n]['height']
        for n in neighbors if n in contents)
    return basin


def inside(pos, heightmap, size):
    out_of_bounds = pos not in heightmap
    filled = heightmap[pos]['basin'] if not out_of_bounds else False
    basin = test_basin(contents=heightmap, position=pos, size=size) \
        if not out_of_bounds else False
    inside_ = not out_of_bounds and not filled and basin
    return inside_
```

| Contents                   | Command           | Answer   | Time     |
|----------------------------|-------------------|----------|----------|
| [`input.txt`](./input.txt) | `./day_9.py -p 2` | `827904` | 158.9 ms | 
