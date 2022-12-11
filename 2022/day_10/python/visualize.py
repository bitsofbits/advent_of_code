"""Attempt to visualize the results using curses
"""
import curses
import time

from implementation import execute, load_program

blank_raster = (("·" * 40 + "\n") * 6)[:-1]


def render_states(states):
    """Render outputs as a series of text raster"""
    raster = ""
    for cycle, value in states:
        ndx = cycle - 1
        col = ndx % 40
        if ndx > 0 and ndx % 40 == 0:
            raster += "\n"
        is_lit = col in {value - 1, value, value + 1}
        raster += "@" if is_lit else " "
        yield raster + blank_raster[len(raster) :]


def char_at(raster, row, col):
    if not 0 <= row < 6:
        return None
    if not 0 <= col <= 40:
        return None
    return raster[row * 41 + col]


def get_sprint_cols(value):
    return {max(min(value + offset, 39), 0) for offset in [-1, 0, 1]}


def visualize(delay):
    curses.start_color()
    curses.use_default_colors()
    states = list(execute(load_program("data/program.txt")))
    pad = 2
    height = 7 + pad
    width = 40 + pad
    win = curses.newwin(height, width, 0, 0)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    for i, line in enumerate(blank_raster.split("\n")):
        win.addstr(i + pad, pad, line, curses.color_pair(4))
    win.refresh()
    time.sleep(20 * delay)
    for (state, raster) in zip(states, render_states(states)):
        for i, line in enumerate(raster.split("\n")):
            win.addstr(i + pad, pad, line, curses.color_pair(4))

        cycle, value = state
        row, col = divmod(cycle - 1, 40)

        sprite_cols = get_sprint_cols(value)
        for scol in sprite_cols:
            char = char_at(raster, row, scol)
            win.addch(row + pad, scol + pad, char, curses.color_pair(1))

        char = char_at(raster, row, col)
        if col in sprite_cols:
            win.addch(row + pad, col + pad, char, curses.color_pair(2))
        else:
            win.addch(row + pad, col + pad, char, curses.color_pair(3))

        time.sleep(delay)
        win.refresh()

    for i, line in enumerate(raster.split("\n")):
        win.addstr(i + pad, pad, line, curses.color_pair(4))
    win.refresh()
    time.sleep(20 * delay)


if __name__ == "__main__":
    curses.wrapper(lambda x: visualize(delay=0.05))
