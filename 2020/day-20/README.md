# Day 20: Jurassic Jigsaw

Goal is to match borders of a number of bitmaps which may rotated and/or flipped.

## Content Decoding

Bitmaps are serialized following a pattern.

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

Tile 6789:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

(...)
```

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

Bits located inside the array (meaning not on any border nor edges) are not relevant for part one.

Thus the remaining relevant content is:
* Tile identifier
* All four borders

Each border contains ten binary pixels, and can be expressed as an integer between 0 and 1023.
