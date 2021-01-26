
def part2(lines):
    tiles = dict(read(lines))
    img = assemble(tiles)
    img = concat(img)
    print(0)


def read(lines):
    tiles = "".join(lines).split("\n\n")
    for title, tile in (t.rstrip().split("\n", maxsplit=1) for t in tiles):
        tid = int(title.rstrip(":").split(maxsplit=1)[1])
        yield tid, list(parse(tile))


def parse(tile):
    tile = [list(r) for r in tile.replace("#", "1").replace(".", "0").splitlines()]
    for i in range(8):
        yield borders(tile), tile
        tile = list(rotate(tile))
        if i == 3:
            tile = [r[::-1] for r in tile]


def rotate(tile):
    for x in range(len(tile[0])):
        yield [r[-x - 1] for r in tile]


def borders(tile):
    left = int("".join(t[0] for t in tile), 2)
    right = int("".join(t[-1] for t in tile), 2)
    top = int("".join(tile[0]), 2)
    bot = int("".join(tile[-1]), 2)
    return left, right, top, bot


def assemble(tiles):
    size = int(len(tiles) ** 0.5)
    return assemble_dfs(tiles, [[None] * size for _ in range(size)], set())


def assemble_dfs(tiles, img, placed, row=0, col=0):
    rc = row, col + 1
    if col == len(img) - 1:
        rc = row + 1, 0
    for tid, tile in tiles.items():
        if tid not in placed:
            placed.add(tid)
            for i, ((left, right, top, bot), ith_tile) in enumerate(tile):
                if (row > 0 and img[row - 1][col][1] != top) or (
                    col > 0 and img[row][col - 1][0] != left
                ):
                    continue
                img[row][col] = right, bot, tid, i, ith_tile
                assemble_dfs(tiles, img, placed, *rc)
                if len(placed) == len(tiles):
                    return img
            placed.remove(tid)


def concat(img):
    size = len(img) * (len(img[0][0][-1]) - 2)
    final_img = [[] for _ in range(size)]
    r = 0
    for row in img:
        for *_, tile in row:
            for y, line in enumerate(tile[1:-1]):
                final_img[r + y] += line[1:-1]
        r += len(tile) - 2
    return final_img


if __name__ == '__main__':
    part2(open('input.txt'))
