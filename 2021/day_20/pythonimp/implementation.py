from math import inf

EXAMPLE_TEXT = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


def render(img):
    min_i = min(i for (i, j) in img)
    min_j = min(j for (i, j) in img)
    max_i = max(i for (i, j) in img)
    max_j = max(j for (i, j) in img)
    text = ""
    for i in range(min_i, max_i + 1):
        text += "|"
        for j in range(min_j, max_j + 1):
            text += ".#"[img[i, j]]
        text += "|\n"
    return text[:-1]


def parse(text):
    """
    >>> filt, img = parse(EXAMPLE_TEXT)
    >>> filt[:4]
    [0, 0, 1, 0]
    >>> print(render(img))
    |#..#.|
    |#....|
    |##..#|
    |..#..|
    |..###|"""
    mapping = {"#": 1, ".": 0}
    filt, img_text = text.strip().split("\n\n")
    filt = filt.strip().replace("\n", "")
    filt = [mapping[c] for c in filt.strip()]
    assert len(filt) == 512, len(filt)
    img = {}
    for i, row in enumerate(img_text.split("\n")):
        for j, c in enumerate(row):
            img[i, j] = mapping[c]
    return filt, img


def compute_extent(img):
    min_i = min_j = inf
    max_i = max_j = -inf
    for i, j in img:
        min_i = min(i, min_i)
        min_j = min(j, min_j)
        max_i = max(i, max_i)
        max_j = max(j, max_j)
    return min_i, max_i, min_j, max_j


def convolve(filt, img, extent, invert=False):
    """
    >>> filt, img = parse(EXAMPLE_TEXT)
    >>> extent = compute_extent(img)
    >>> img = convolve(filt, img, extent)
    >>> print(render(img))
    |.##.##.|
    |#..#.#.|
    |##.#..#|
    |####..#|
    |.#..##.|
    |..##..#|
    |...#.#.|
    >>> img = convolve(filt, img, pad_extent(extent))
    >>> print(render(img))
    |.......#.|
    |.#..#.#..|
    |#.#...###|
    |#...##.#.|
    |#.....#.#|
    |.#.#####.|
    |..#.#####|
    |...##.##.|
    |....###..|
    """
    min_i, max_i, min_j, max_j = extent
    H = max_i - min_i + 5
    W = max_j - min_j + 5
    raster = [invert] * (H * W)
    for (i, j), v in img.items():
        raster[(i - min_i + 2) * W + (j - min_j + 2)] = v
    offsets = [di * W + dj for di in [-1, 0, 1] for dj in [-1, 0, 1]]

    new_img = {}

    for i in range(min_i - 1, max_i + 2):
        k0 = (i - min_i + 2) * W - (min_j - 2)
        for j in range(min_j - 1, max_j + 2):
            k = k0 + j
            ndx = 0
            for os in offsets:
                ndx = 2 * ndx + raster[k + os]
            new_img[i, j] = filt[ndx]
    return new_img


def convolve_twice(filt, img, extent):
    """
    >>> filt, img = parse(EXAMPLE_TEXT)
    >>> extent = compute_extent(img)
    >>> img = convolve(filt, img, extent)
    >>> print(render(img))
    |.##.##.|
    |#..#.#.|
    |##.#..#|
    |####..#|
    |.#..##.|
    |..##..#|
    |...#.#.|
    >>> img = convolve(filt, img, pad_extent(extent))
    >>> print(render(img))
    |.......#.|
    |.#..#.#..|
    |#.#...###|
    |#...##.#.|
    |#.....#.#|
    |.#.#####.|
    |..#.#####|
    |...##.##.|
    |....###..|
    """
    min_i, max_i, min_j, max_j = extent
    H = max_i - min_i + 7
    W = max_j - min_j + 7
    raster = [0] * (H * W)
    for (i, j), v in img.items():
        raster[(i - min_i + 3) * W + (j - min_j + 3)] = v
    offsets = [di * W + dj for di in [-1, 0, 1] for dj in [-1, 0, 1]]

    new_raster = [filt[0] == 1] * (H * W)
    for i in range(min_i - 1, max_i + 2):
        k0 = (i - min_i + 3) * W - (min_j - 3)
        for j in range(min_j - 1, max_j + 2):
            k = k0 + j
            ndx = 0
            for os in offsets:
                ndx = 2 * ndx + raster[k + os]
            new_raster[k] = filt[ndx]

    img = {}

    for i in range(min_i - 2, max_i + 3):
        k0 = (i - min_i + 3) * W - (min_j - 3)
        for j in range(min_j - 2, max_j + 3):
            k = k0 + j
            ndx = 0
            for os in offsets:
                ndx = 2 * ndx + new_raster[k + os]
            img[i, j] = filt[ndx]
    return img


def pad_extent(extent, n=1):
    min_i, max_i, min_j, max_j = extent
    return (min_i - n, max_i + n, min_j - n, max_j + n)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    35
    """
    filt, img = parse(text)
    extent = compute_extent(img)
    img = convolve_twice(filt, img, extent)
    return sum(img.values())


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    3351
    """
    filt, img = parse(text)
    extent = compute_extent(img)
    for i in range(25):
        img = convolve_twice(filt, img, extent)
        extent = pad_extent(extent, 2)
    return sum(img.values())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
