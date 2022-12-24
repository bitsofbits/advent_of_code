import curses
import time

from implementation import Valley


def draw(win, valley):
    for i, line in enumerate(str(valley).split("\n")):
        for j, c in enumerate(line):
            match c:
                case "#":
                    clr = 2
                case "E":
                    clr = 4
                case ".":
                    c = " "
                    clr = 2
                case _:
                    clr = 2
                    c = "·"
            win.addch(i, j, c, curses.color_pair(clr))


def visualize(delay):
    curses.start_color()
    curses.use_default_colors()
    with open("data/data.txt") as f:
        text = f.read()
    valley = Valley(text)
    path = valley.simple_traverse()
    valley = Valley(text)

    width = valley.max_j + 2
    height = valley.max_i + 2
    win = curses.newwin(height + 1, width + 1, 0, 0)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.curs_set(0)

    draw(win, valley)
    win.refresh()
    time.sleep(20 * delay)
    i, j = valley.loc
    for c in path:
        i, j = valley.move(i, j, c)
        valley.loc = (i, j)
        valley.advance_blizzards()
        draw(win, valley)
        win.refresh()
        time.sleep(delay)

    # cave = Cave(text, has_floor=True)
    # draw(win, cave, ex)
    # win.refresh()
    # time.sleep(1000 * delay)

    # dx, _, dy, _ = ex
    # while (pt := cave.drop_sand()) is not None:
    #     cave.blocks[pt] = "o"
    #     (j, i) = pt
    #     assert 0 <= i - dy <= height, (i, dy, height, ex)
    #     assert 0 <= j - dx <= width, (j, dx, width, ex)
    #     win.addch(i - dy, j - dx, "o", curses.color_pair(3))
    #     win.refresh()
    #     time.sleep(delay)
    win.refresh()
    time.sleep(20 * delay)


if __name__ == "__main__":
    curses.wrapper(lambda x: visualize(delay=0.03))
