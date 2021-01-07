# Day 20: Jurassic Jigsaw

Goal is to match borders of a number of bitmaps which may rotated and/or flipped.

## Content Decoding

### Tile Data Extraction

Bitmaps are serialized following a common pattern.

```
Tile 1234:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###
```
* String ``Tile`` followed by an integer
* A 10x10 binary array, with the states ``#`` and ``.`` 


First order of business is to load contents, no need to go fancy just yet.

```python
tile = dict()
for line in open(file):
    if 'Tile ' in line:
        tile['id'] = int(line[5:-2])
        tile['rows'] = list()
    elif len(line) > 2:
        tile['rows'].append(line.strip())
        last_row = len(tile['rows']) == len(line.strip())
        if last_row:
            yield tile
            tile = dict()
```

### Tile Border Computation

The day 20 challenge only uses border data, leaving out all data not part of the tile borders.

Extracting top and bottom borders is straightforward, however the tile needs to be rotated to facilitate extraction of the two remaining borders.
```python
rows = tile['rows']
rot_cw = list(''.join(c) for c in zip(*rows[::-1]))
```

Since tiles may be flipped, borders may also be reversed. After converting borders into a list of integer.

### Submission Calculation

Corner tiles can be extracted by matching tiles with only two border matches.

```python
corner_tiles = [k for k, v in matched_tiles.items() if len(v) == 2]
corners_id_product = functools.reduce(operator.mul, corner_tiles)
```
