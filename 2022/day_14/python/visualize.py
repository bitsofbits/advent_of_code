import curses
import time

from implementation import Cave


def draw(win, cave, ex):
    for i, line in enumerate(cave.as_string(ex).split("\n")):
        for j, c in enumerate(line):
            win.addch(i, j, c, curses.color_pair(2))


def visualize(delay):
    curses.start_color()
    curses.use_default_colors()
    with open("data/data.txt") as f:
        text = f.read()
    sacrificial_cave = Cave(text, has_floor=True)
    sacrificial_cave.fill_with_sand()
    ex = sacrificial_cave.find_extent()

    width = ex.x1 - ex.x0 + 1
    height = ex.y1 - ex.y0 + 2
    win = curses.newwin(height + 1, width + 1, 0, 0)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.curs_set(0)

    cave = Cave(text, has_floor=True)
    draw(win, cave, ex)
    win.refresh()
    time.sleep(1000 * delay)

    dx, _, dy, _ = ex
    while (pt := cave.drop_sand()) is not None:
        cave.blocks[pt] = "o"
        (j, i) = pt
        assert 0 <= i - dy <= height, (i, dy, height, ex)
        assert 0 <= j - dx <= width, (j, dx, width, ex)
        win.addch(i - dy, j - dx, "o", curses.color_pair(3))
        win.refresh()
        time.sleep(delay)
    win.refresh()
    time.sleep(10000 * delay)


if __name__ == "__main__":
    curses.wrapper(lambda x: visualize(delay=0.0002))
