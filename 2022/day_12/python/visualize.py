import curses
import time

from implementation import Map

pallete = r"""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """[
    ::-1
]


def getch(mp, pt):
    if pt == mp.start:
        return "S"
    elif pt == mp.end:
        return "E"
    else:
        return pallete[mp.data[pt] + 1]


def draw(win, mp):
    for i in range(mp.data.shape[0]):
        for j in range(mp.data.shape[1]):
            pt = (i, j)
            c = getch(mp, pt)
            win.addch(i, j, c, curses.color_pair(2))


def visualize(delay):
    curses.start_color()
    curses.use_default_colors()
    mp = Map("data/data.txt")
    width = mp.data.shape[1]
    height = mp.data.shape[0]
    win = curses.newwin(height + 1, width + 1, 0, 0)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_RED)

    draw(win, mp)
    win.refresh()

    start, nodes = mp.sample_forward(0)
    for pt, _ in nodes:
        i, j = pt
        c = getch(mp, pt)
        win.addch(i, j, c, curses.color_pair(3))
        win.refresh()
        time.sleep(delay)
    time.sleep(100 * delay)
    path = mp.sample_back(nodes, start)
    for pt in path:
        i, j = pt
        c = getch(mp, pt)
        win.addch(i, j, c, curses.color_pair(4))
        win.refresh()
        time.sleep(10 * delay)
    time.sleep(200 * delay)

    win.refresh()
    time.sleep(100 * delay)


if __name__ == "__main__":
    curses.wrapper(lambda x: visualize(delay=0.002))
