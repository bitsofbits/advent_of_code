from typing import NamedTuple


def _parse_node(text):
    return tuple(int(x.strip()) for x in text.strip().split(","))


example_text = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


class Extent(NamedTuple):
    x0: int
    x1: int
    y0: int
    y1: int


class Cave:
    """
    >>> c = Cave(example_text)
    >>> print(c)
    ··········
    ··········
    ··········
    ··········
    ····#···##
    ····#···#·
    ··###···#·
    ········#·
    ········#·
    #########·
    >>> c = Cave(example_text)
    >>> c.fill_with_sand()
    24
    >>> print(c)
    ··········
    ··········
    ······o···
    ·····ooo··
    ····#ooo##
    ···o#ooo#·
    ··###ooo#·
    ····oooo#·
    ·o·ooooo#·
    #########·
    >>> c = Cave(example_text, has_floor=True)
    >>> c.fill_with_sand()
    93
    >>> print(c)
    ··········o··········
    ·········ooo·········
    ········ooooo········
    ·······ooooooo·······
    ······oo#ooo##o······
    ·····ooo#ooo#ooo·····
    ····oo###ooo#oooo····
    ···oooo·oooo#ooooo···
    ··oooooooooo#oooooo··
    ·ooo#########ooooooo·
    ooooo·······ooooooooo
    #####################
    """

    inlet = (500, 0)

    def __init__(self, text, has_floor=False):
        self.blocks = self.parse(text)
        self.extent = self.find_extent()
        self.has_floor = has_floor

    def parse(self, text):
        blocks = {}
        for line in text.strip().split("\n"):
            nodes = [_parse_node(x) for x in line.split("->")]
            last = nodes[0]
            for nd in nodes[1:]:
                x0, y0 = last
                x1, y1 = nd
                dx, dy = ((a - b) for (a, b) in zip(nd, last))
                match (dx, dy):
                    case (v, 0) if v > 0:
                        for i in range(0, v + 1):
                            blocks[x0 + i, y0] = "#"
                    case (v, 0) if v < 0:
                        for i in range(v, 1):
                            blocks[x0 + i, y0] = "#"
                    case (0, v) if v > 0:
                        for i in range(0, v + 1):
                            blocks[x0, y0 + i] = "#"
                    case (0, v) if v < 0:
                        for i in range(v, 1):
                            blocks[x0, y0 + i] = "#"
                    case _:
                        raise ValueError()
                last = nd
        return blocks

    def blocked(self, x, y):
        if (x, y) in self.blocks:
            return True
        if self.has_floor and y >= self.extent.y1 + 2:
            return True
        return False

    def fell_into_the_abyss(self, x, y):
        if self.has_floor:
            return False
        ex = self.extent
        return not (ex.x0 <= x <= ex.x1 and ex.y0 <= y <= ex.y1)

    def drop_sand(self):
        x, y = self.inlet
        if self.blocked(x, y):
            return None
        while True:
            if self.fell_into_the_abyss(x, y):
                return None
            if not self.blocked(x, y + 1):
                y += 1
            elif not self.blocked(x - 1, y + 1):
                y += 1
                x -= 1
            elif not self.blocked(x + 1, y + 1):
                y += 1
                x += 1
            else:
                return x, y

    def fill_with_sand(self):
        while (pt := self.drop_sand()) is not None:
            self.blocks[pt] = "o"
        return sum(1 for x in self.blocks.values() if x == "o")

    def find_extent(self):
        xi, yi = self.inlet
        x0 = min(xi, min(x for (x, y) in self.blocks.keys()))
        x1 = max(xi, max(x for (x, y) in self.blocks.keys()))
        y0 = min(yi, min(y for (x, y) in self.blocks.keys()))
        y1 = max(yi, max(y for (x, y) in self.blocks.keys()))
        return Extent(x0, x1, y0, y1)

    def as_string(self, extent):
        x0, x1, y0, y1 = extent
        dx = x1 - x0 + 1
        dy = y1 - y0 + 1
        text = ""
        for i in range(dy):
            y = y0 + i
            for j in range(dx):
                x = x0 + j
                text += self.blocks.get((x, y), "·")
            text += "\n"
        if self.has_floor:
            text += "#" * dx + "\n"
        return text[:-1]

    def __str__(self):
        return self.as_string(self.find_extent())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
