import curses
import time
from itertools import count

from implementation import Cave
from matplotlib import cm

# use viridis to get colors in 0, 1 space


def draw(win, cave, when, ex):
    scale = (256 - 8) / max(when.values())
    for i, line in enumerate(cave.as_string(ex).split("\n")):
        for j, c in enumerate(line):
            if c == "#":
                win.addch(i, j, " ", curses.color_pair(3))
            else:
                win.addch(i, j, " ", curses.color_pair(2))
    for (i, j), n in when.items():
        ndx = int(scale * n) + 4
        win.addch(j - ex.y0, i - ex.x0, "·", curses.color_pair(ndx))


def re(x):
    return int(round(1000 * x))


def visualize(delay):
    # This is an attempt to create the beautiful visualization by Jonathon Carroll
    curses.start_color()
    curses.use_default_colors()
    N_COLORS = 256
    has_floor = False
    for n in range(8, N_COLORS):
        x = (n - 8) / (N_COLORS - 8)
        r, g, b, _ = cm.plasma(x)
        # assert False, (re(r), re(b), re(g))
        curses.init_color(n, re(r), re(g), re(b))
    for n, i in enumerate(range(4, curses.COLORS - 8)):
        curses.init_pair(i, -1, n + 8)
    with open("data/data.txt") as f:
        text = f.read()
    sacrificial_cave = Cave(text, has_floor=has_floor)
    sacrificial_cave.fill_with_sand()
    ex = sacrificial_cave.find_extent()

    width = ex.x1 - ex.x0 + 1
    height = ex.y1 - ex.y0 + 2
    win = curses.newwin(height + 1, width + 1, 0, 0)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.curs_set(0)

    cave = Cave(text, has_floor=has_floor)
    when = {}
    for i in count():
        pt = cave.drop_sand()
        cave.blocks[pt] = "o"
        if pt is None:
            break
        when[pt] = i
    cave = Cave(text, has_floor=True)

    draw(win, cave, when, ex)
    win.refresh()
    time.sleep(100000 * delay)


if __name__ == "__main__":
    curses.wrapper(lambda x: visualize(delay=0.0002))
