from implementation import Map

pallete = r"""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """[
    ::-1
]


def visualize(start_values):
    mp = Map("data/data.txt")
    points = set(mp.find_shortest_path(start_values))
    raster = ""
    for i, r in enumerate(mp.rows):
        for j, c in enumerate(r):
            if (i, j) in points:
                c = pallete[-1]
            elif "a" <= c <= "z":
                ndx = (ord(c) - ord("a")) + 1
                c = pallete[ndx]
            raster += c
        raster += "\n"

    print(raster)


if __name__ == "__main__":
    visualize(start_values={"S"})
    # visualize(start_values={"S", "a"})
