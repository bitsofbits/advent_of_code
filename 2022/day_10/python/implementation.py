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
