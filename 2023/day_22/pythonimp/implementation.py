def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:2]
    [('A', (1, 0, 1), (1, 2, 1)), ('B', (0, 0, 2), (2, 0, 2))]
    """
    bricks = []
    for i, line in enumerate(text.strip().split('\n')):
        start, end = line.split('~')
        tag = chr(ord('A') + i)
        bricks.append(
            (
                tag,
                tuple(int(x) for x in start.split(',')),
                tuple(int(x) for x in end.split(',')),
            )
        )
    return bricks


def reorient_bricks(bricks):
    for tag, start, end in bricks:
        if start[-1] > end[-1]:
            tag, start, end = tag, end, start
        yield tag, start, end


def sign(x):
    return int(x > 0) - int(x < 0)


# def drop_bricks(bricks, announce=False, truncate=False):
#     bricks = sorted(bricks, key=lambda x: x[1][-1])
#     bottom = {}
#     highest_z0 = 0
#     for tag, start, end in bricks:
#         x0, y0, z0 = start
#         x1, y1, z1 = end
#         assert z0 <= z1
#         assert z0 >= highest_z0
#         highest_z0 = z0
#         dx, dy, dz = (b - a for (a, b) in zip(start, end))
#         sx, sy, sz = (sign(a) for a in (dx, dy, dz))
#         length = max((x for x in (dx, dy, dz)), key=abs)
#         if length < 0:
#             length, sx, sy, sz = -length, -sx, -sy, -sz
#         assert (
#             x0 + length * sx == x1 and y0 + length * sy == y1 and z0 + length * sz == z1
#         )

#         new_z = (
#             max(bottom.get((x0 + i * sx, y0 + i * sy), 0) for i in range(length + 1))
#             + 1
#         )

#         delta = z0 - new_z
#         assert delta >= 0

#         new_brick = tag, (x0, y0, z0 - delta), (x1, y1, z1 - delta)
#         for i in range(length + 1):
#             bottom[x0 + i * sx, y0 + i * sy] = max(
#                 z0 + i * sz - delta, bottom.get((x0 + i * sx, y0 + i * sy), 0)
#             )
#         if announce and delta > 0:
#             print("droppping" if (delta > 0) else "not dropping", start, end)
#             print("to", new_brick)
#             print(bottom)
#         if truncate and delta > 0:
#             return

#         yield new_brick


def drop_bricks(bricks, announce=False, truncate=False):
    bricks = sorted(bricks, key=lambda x: x[1][-1])
    bottom = {}
    resting_on = {}
    highest_z0 = 0
    new_bricks = []
    for tag, start, end in bricks:
        x0, y0, z0 = start
        x1, y1, z1 = end
        assert z0 <= z1
        assert z0 >= highest_z0
        highest_z0 = z0
        dx, dy, dz = (b - a for (a, b) in zip(start, end))
        sx, sy, sz = (sign(a) for a in (dx, dy, dz))
        length = max((x for x in (dx, dy, dz)), key=abs)
        if length < 0:
            length, sx, sy, sz = -length, -sx, -sy, -sz
        assert (
            x0 + length * sx == x1 and y0 + length * sy == y1 and z0 + length * sz == z1
        )

        highest_point_of_contact = max(
            bottom.get((x0 + i * sx, y0 + i * sy), (0, None))[0]
            for i in range(length + 1)
        )

        touching = []
        for i in range(length + 1):
            key = (x0 + i * sx, y0 + i * sy)
            height, what = bottom.get(key, (0, None))
            if height == highest_point_of_contact:
                touching.append(what)
            else:
                touching.append('')
        new_z = highest_point_of_contact + 1

        # print(tag, touching)

        delta = z0 - new_z
        assert delta >= 0

        new_brick = tag, (x0, y0, z0 - delta), (x1, y1, z1 - delta)
        for i in range(length + 1):
            key = (x0 + i * sx, y0 + i * sy)
            bottom[key] = (
                max(z0 + i * sz - delta, bottom.get((x0 + i * sx, y0 + i * sy)[0], 0)),
                tag,
            )

        resting_on[tag] = set(x for x in touching if x != '')
        if announce and delta > 0:
            print("droppping" if (delta > 0) else "not dropping", start, end)
            print("to", new_brick)
            print(bottom)
        if truncate and delta > 0:
            return new_bricks, resting_on

        new_bricks.append(new_brick)

    return new_bricks, resting_on


# TODO: try making a map of what brick sit on what and see if we can use to speed up.
# Maybe generating while dropping bricks


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    5

    """
    bricks = list(reorient_bricks(parse(text)))
    bricks, resting_on = drop_bricks(bricks)
    bricks = sorted(bricks, key=lambda x: x[1][-1])
    count = 0
    for i, brick in enumerate(bricks):
        tag, *_ = brick
        removed = {tag}
        for brick in bricks[i + 1 :]:
            tag, *_ = brick
            if not resting_on[tag] - removed:
                break
        else:
            count += 1
    return count


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    7

    97452 is too low
    """
    bricks = list(reorient_bricks(parse(text)))
    bricks, resting_on = drop_bricks(bricks)
    bricks = sorted(bricks, key=lambda x: x[1][-1])
    count = 0
    for i in range(len(bricks) - 1):
        tag, *_ = bricks[i]
        removed = {tag}
        for j, brick in enumerate(bricks[i + 1 :]):
            tag, *_ = brick
            if resting_on[tag] - removed:
                count += j
                break
            removed.add(tag)
        else:
            count += j + 1

    return count


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
