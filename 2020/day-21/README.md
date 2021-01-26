# Day 21: Allergen Assessment

Goal is to determine which ingredients cannot possibly contain any of the allergens in your list.

## Content Decoding

Contents are formatted in a series of **lines**. Each line has **two parts**: a **list of ingredients** and a **list of some or all allergens** in parenthesizes. Both lists contain items separated by single space characters.

```
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
```

After decoding:

```python
line = {
    'ingredients': ['mxmxvkd', 'kfcds', 'sqjhc', 'nhms'],
    'some_allergens': ['dairy', 'fish'],
}
```

### Multiple Stage Split Decoding

This decoding methods involves a number of split stages:

1. Remove trailing closing parenthesis
1. Split lines using `` (contains `` as separator.
    1. Left hand side is then split using space character as separator.
    1. Right hand side is then split using space character as separator.
1. Group lists in a dictionary structure.

```python
for line in lines:
    line: str = line.strip()[:-1]
    lhs, rhs = line.split(' (contains ')
    ingredients: list = lhs.split(' ')
    allergens: list = rhs.split(' ')
    yield {
        'ingredients': ingredients,
        'some_allergens': allergens,
    }
```

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

# Part Two

Had to go through several iterations to get this one right.

