import sys


class List2D:
    def __init__(self, data, shape):
        assert len(shape) == 2
        assert len(data) == shape[0] * shape[1]
        self.data = data
        self.shape = shape

    def __getitem__(self, ndx):
        i, j = ndx
        assert 0 <= i < self.shape[0]
        assert 0 <= j < self.shape[1]
        return self.data[i * self.shape[1] + j]

    def __setitem__(self, ndx, value):
        i, j = ndx
        assert 0 <= i < self.shape[0]
        assert 0 <= j < self.shape[1]
        self.data[i * self.shape[1] + j] = value

    def __str__(self):
        lines = []
        di, dj = self.shape
        for i in range(di):
            lines.append("".join(x for x in self.data[i * dj : (i + 1) * dj]))
        return "\n".join(lines)


def execute(program):
    x = 1
    cycle = 0
    for opset in program:
        match opset:
            case ("noop",):
                cycle += 1
                yield cycle, x
            case ("addx", arg):
                cycle += 1
                yield cycle, x
                cycle += 1
                yield cycle, x
                x += arg
            case _:
                raise ValueError(opset)


def signal_sum(outputs):
    """Sum the "signal" at the specified values of cycles

    >>> signal_sum(execute(load_program("data/example_program.txt")))
    13140
    """
    probe_cycles = {20, 60, 100, 140, 180, 220}
    total = 0
    for cycle, value in outputs:
        if cycle in probe_cycles:
            total += value * cycle
    return total


def render(outputs):
    """Render outputs as a text raster

    >>> raster = render(execute(load_program("data/example_program.txt")))
    >>> print(raster)
    ##..##..##..##..##..##..##..##..##..##..
    ###...###...###...###...###...###...###.
    ####....####....####....####....####....
    #####.....#####.....#####.....#####.....
    ######......######......######......####
    #######.......#######.......#######.....
    """
    raster = ""
    for cycle, value in outputs:
        ndx = cycle - 1
        col = ndx % 40
        if ndx > 0 and ndx % 40 == 0:
            raster += "\n"
        is_lit = col in {value - 1, value, value + 1}
        raster += "#" if is_lit else "."
    return raster


def load_program(path):
    with open(path) as f:
        for line in f:
            match line.strip().split():
                case ("addx" as cmd, arg):
                    yield (cmd, int(arg))
                case ("noop" as cmd,):
                    yield (cmd,)
                case _:
                    raise ValueError(line)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
