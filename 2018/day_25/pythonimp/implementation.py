from collections import defaultdict


def parse(text):
    """
    >>> sorted(parse(EXAMPLE_TEXT))[:2]
    [(0, 0, 0, 0), (0, 0, 0, 3)]
    """
    return frozenset(
        tuple(int(x) for x in line.split(',')) for line in text.strip().split()
    )


# function MakeSet(x) is
#     if x is not already in the forest then
#         x.parent := x
#         x.size := 1     // if nodes store size
#         x.rank := 0     // if nodes store rank
#     end if
# end function
# function Find(x) is
#     if x.parent ≠ x then
#         x.parent := Find(x.parent)
#         return x.parent
#     else
#         return x
#     end if
# end function

# function Union(x, y) is
#     // Replace nodes by roots
#     x := Find(x)
#     y := Find(y)

#     if x = y then
#         return  // x and y are already in the same set
#     end if

#     // If necessary, swap variables to ensure that
#     // x has at least as many descendants as y
#     if x.size < y.size then
#         (x, y) := (y, x)
#     end if

#     // Make x the new root
#     y.parent := x
#     // Update the size of x
#     x.size := x.size + y.size
# end function


def find(x, forest):
    parent = forest[x]
    if parent != x:
        forest[x] = find(parent, forest)
        return forest[x]
        # return find(parent, forest)
    else:
        return x


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    2

    >>> part_1(EXAMPLE2_TEXT)
    4

    >>> part_1(EXAMPLE3_TEXT)
    3

    >>> part_1(EXAMPLE4_TEXT)
    8
    """
    locations = parse(text)
    nearby = defaultdict(set)
    for point in locations:
        x0, y0, z0, t0 = point
        for dx in range(-3, 4):
            x = x0 + dx
            for dy in range(-3, 4):
                y = y0 + dy
                for dz in range(-3, 4):
                    z = z0 + dz
                    for dt in range(-3, 4):
                        if 0 < abs(dx) + abs(dy) + abs(dz) + abs(dt) <= 3:
                            t = t0 + dt
                            nearby[x, y, z, t].add(point)
    nearby = dict(nearby)

    forest = {v: v for v in locations}
    while True:
        for point, parent in forest.items():
            # if point == parent:
            # is root
            parent = find(point, forest)
            for potential_parent in nearby.get(point, ()):
                potential_parent = find(potential_parent, forest)
                assert forest[potential_parent] == potential_parent
                # print(potential_parent, point)
                if potential_parent != parent:
                    forest[parent] = potential_parent
                    break
            else:
                continue
            break
        else:
            break

    # for point in locations:
    #     assert point not in forest
    #     for potential_parent in nearby[point]:
    #         if potential_parent in forest:
    #             parent = find(potential_parent, forest)
    #             forest[point] = parent
    #             break
    #     else:
    #         forest[point] = point

    # print(forest)
    # print(len(forest), len(locations))

    return sum(k == v for (k, v) in forest.items())


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    with open(data_dir / "example3.txt") as f:
        EXAMPLE3_TEXT = f.read()
    with open(data_dir / "example4.txt") as f:
        EXAMPLE4_TEXT = f.read()
    doctest.testmod()
