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


def convolve(filt, img, invert=False):
    """
    >>> filt, img = parse(EXAMPLE_TEXT)
    >>> img = convolve(filt, img)
    >>> print(render(img))
    |.##.##.|
    |#..#.#.|
    |##.#..#|
    |####..#|
    |.#..##.|
    |..##..#|
    |...#.#.|
    >>> img = convolve(filt, img)
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
    min_i = min_j = inf
    max_i = max_j = -inf
    for i, j in img:
        min_i = min(i, min_i)
        min_j = min(j, min_j)
        max_i = max(i, max_i)
        max_j = max(j, max_j)
    new_img = {}

    for i in range(min_i - 1, max_i + 2):
        for j in range(min_j - 1, max_j + 2):
            x = 0
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    x = 2 * x + img.get((i + di, j + dj), invert)
            new_img[i, j] = filt[x]
    return new_img


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    35

    5698 too high
    5633 too high

    5563?
    """
    filt, img = parse(text)
    invert = filt[0] == 1
    img = convolve(filt, img)
    img = convolve(filt, img, invert)
    return sum(img.values())


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    3351
    """
    filt, img = parse(text)
    invert = filt[0] == 1
    for i in range(25):
        img = convolve(filt, img)
        img = convolve(filt, img, invert)
    return sum(img.values())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
