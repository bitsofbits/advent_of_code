"""Attempt to visualize the results using curses
"""
import curses
import time

from implementation import Monkey, load_monkeys


def char_at(raster, row, col, width, height):
    if not 0 <= row < height:
        return None
    if not 0 <= col <= width:
        return None
    return raster[row * (width + 1) + col]


def get_sprint_cols(value):
    return {max(min(value + offset, 39), 0) for offset in [-1, 0, 1]}


def visualize(delay):
    curses.start_color()
    curses.use_default_colors()
    monkeys = load_monkeys("data/data.txt", 3)
    dx_pad = 4
    dy_pad = 2
    spacing = 6
    height = 30
    n = len(monkeys)
    width = 2 * dx_pad + n + (n - 1) * spacing
    win = curses.newwin(height + 1, width + 1, 0, 0)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)

    curses.curs_set(0)

    def display(monkeys, highlight):
        win.clear()
        for i in range(height):
            win.addstr(i, 0, " " * width, curses.color_pair(2))
        for m in monkeys.values():
            x = dx_pad + m.identifier * (spacing + 1)
            y = height - dy_pad - 2
            if m.identifier == highlight:
                win.addch(y, x, "M", curses.color_pair(4))
            else:
                win.addch(y, x, "M", curses.color_pair(2))
            for i, _ in enumerate(m.items):

                assert y - i - 1 > 0, y - i - 1
                win.addch(y - i - 1, x, "@", curses.color_pair(3))
        time.sleep(delay)
        win.refresh()

    modulus = 1
    for m in monkeys.values():
        modulus *= m.test_value

    display(monkeys, None)
    for _ in range(20):
        for k in sorted(monkeys):
            for kt, vt in monkeys[k].take_turn(modulus).items():
                monkeys[kt].items.extend(vt)
            display(monkeys, k)
        display(monkeys, None)
        time.sleep(2 * delay)

    time.sleep(10 * delay)


if __name__ == "__main__":
    curses.wrapper(lambda x: visualize(delay=0.1))
