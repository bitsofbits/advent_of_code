import curses
import time

from implementation import Board


def draw(win, board, di, dj):
    win.bkgd(" ", curses.color_pair(2))
    for i, line in enumerate(str(board).strip().split("\n")):
        for j, c in enumerate(line):
            match c:
                case "#":
                    clr = 2
                case "E":
                    clr = 4
                case ".":
                    c = " "
                    clr = 2
                case "|":
                    continue
                case _:
                    clr = 2
                    c = "·"
            try:
                win.addch(i + di, j + dj, c, curses.color_pair(clr))
            except:
                if c != " ":
                    break


def visualize(delay):
    curses.start_color()
    curses.use_default_colors()
    with open("data/data.txt") as f:
        text = f.read()
    board = Board(text)
    board.move_elves(1000)
    i0, i1, j0, j1 = board.extent

    width = j1 - j0 - 1
    height = i1 - i0 - 1
    win = curses.newwin(height + 1, width + 1, 0, 0)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.curs_set(0)

    board = Board(text)
    i, _, j, _ = board.extent
    draw(win, board, i - i0, j - j0 - 1)
    win.refresh()
    time.sleep(20 * delay)
    for i in range(1000):
        board.move_elves(1)
        i, _, j, _ = board.extent
        draw(win, board, i - i0, j - j0 - 1)
        win.refresh()
        time.sleep(delay)
    win.refresh()
    time.sleep(20 * delay)


if __name__ == "__main__":
    curses.wrapper(lambda x: visualize(delay=0.03))
