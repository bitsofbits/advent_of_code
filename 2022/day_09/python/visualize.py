"""Attempt to visualize the results using curses
"""
import curses
import time

from implementation import Rope, load_moves

blank_raster = (("·" * 40 + "\n") * 6)[:-1]


def _compute_extent(rope):
    x = [x for (x, y) in rope.knots]
    y = [y for (x, y) in rope.knots]
    return min(x), max(x), min(y), max(y)


def _update_extent(extent, rope):
    x0, x1, y0, y1 = extent
    X0, X1, Y0, Y1 = _compute_extent(rope)
    return min(x0, X0), max(x1, X1), min(y0, Y0), max(y1, Y1)


def find_max_extent(rope, moves):
    extent = _compute_extent(rope)
    for mv in moves:
        for _ in range(mv.count):
            rope.move(mv.direction)
            extent = _update_extent(extent, rope)
    return extent


def compute_sizes(rope_size, moves, pad):
    rope = Rope(rope_size)
    extent = find_max_extent(rope, moves)
    (x0, x1, y0, y1) = extent
    offset = (max(-x0, 0) + pad, max(-y0, 0) + pad)
    size = (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad
    return offset, size


def render_rope(win, rope, offset, size, trail):
    dx, dy = offset
    nx, ny = size
    last_ndx = len(rope.knots) - 1
    win.clear()
    for i in range(ny):
        win.addstr(i, 0, " " * nx, curses.color_pair(2))

    for (x, y) in trail:
        i = ny - dy - y
        j = x + dx
        win.addch(i, j, "·", curses.color_pair(4))

    for ndx, knt in enumerate(rope.knots):
        x, y = knt
        i = ny - dy - y
        j = x + dx
        if ndx == 0:
            win.addch(i, j, "@", curses.color_pair(2))
        elif ndx == last_ndx:
            win.addch(i, j, "*", curses.color_pair(4))
        else:
            win.addch(i, j, "O", curses.color_pair(3))


def visualize(delay):
    curses.start_color()
    curses.use_default_colors()
    moves = load_moves("data/data.txt")[:800]
    PAD = 1
    rope_size = 10
    rope = Rope(rope_size)
    offset, size = compute_sizes(rope_size, moves, PAD)
    width, height = size
    win = curses.newwin(height + 1, width + 1, 0, 0)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.curs_set(0)

    rope = Rope(rope_size)
    trail_so_far = [rope.tail]
    render_rope(win, rope, offset, size, trail_so_far)
    win.refresh()
    time.sleep(10 * delay)
    for mv in moves:
        for _ in range(mv.count):
            rope.move(mv.direction)
            render_rope(win, rope, offset, size, trail_so_far)
            win.refresh()
            time.sleep(delay)
            trail_so_far.append(rope.tail)

    win.refresh()
    time.sleep(10 * delay)


if __name__ == "__main__":
    curses.wrapper(lambda x: visualize(delay=0.05))
