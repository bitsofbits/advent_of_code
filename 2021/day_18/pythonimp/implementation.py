from ast import literal_eval
from copy import deepcopy

EXAMPLE_TEXT = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""


def parse(text):
    """
    >>> parse("[[[[1,2],[3,4]],[[5,6],[7,8]]],9]")
    [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], 9]
    """
    return literal_eval(text)


def getv(x, ndx):
    """
    >>> getv([[[[[9,8],1],2],3],4], (0, 0, 0, 0))
    [9, 8]
    >>> getv([[[[[9,8],1],2],3],4], (0, 0, 0, 0, 1))
    8
    """
    for i in ndx:
        x = x[i]
    return x


def setv(x, ndx, val):
    """
    >>> val = [[[[[9,8],1],2],3],4]
    >>> setv(val, (0, 0, 0, 0, 1), 2)
    >>> setv(val, (0, 0, 1), 3)
    >>> val
    [[[[[9, 2], 1], 3], 3], 4]
    """
    for i in ndx[:-1]:
        x = x[i]
    x[ndx[-1]] = val


def indexed(val):
    """
    >>> list(indexed([[1,2],3]))
    [((0, 0), 1), ((0, 1), 2), ((1,), 3)]
    """
    stack = [(val, ())]
    while stack:
        x, ndx = stack.pop()
        if isinstance(x, int):
            yield ndx, x
        else:
            L, R = x
            stack.append((R, (*ndx, 1)))
            stack.append((L, (*ndx, 0)))


def indices_of(val):
    """
    >>> list(indices_of([[1,2],3]))
    [(0, 0), (0, 1), (1,)]
    """
    for (ndx, x) in indexed(val):
        yield ndx


def _reduce_once(x, indices):
    # First check if we need to explode anything
    for i, (ndx, val) in enumerate(indices):
        if len(ndx) == 5:
            lval = val
            _, rval = indices[i + 1]
            if i - 1 >= 0:
                ndx_n, nval = indices[i - 1]
                nval += lval
                setv(x, ndx_n, nval)
                indices[i - 1] = (ndx_n, nval)
            if i + 2 < len(indices):
                ndx_p, pval = indices[i + 2]
                pval += rval
                setv(x, ndx_p, pval)
                indices[i + 2] = (ndx_p, pval)
            setv(x, ndx[:-1], 0)
            # Update indices in place, since regenerating is expensive
            indices[i : i + 2] = [(ndx[:-1], 0)]
            return True
    # Then if we need to split anything
    for i, (ndx, v) in enumerate(indices):
        if v >= 10:
            L = v // 2
            R = v - L
            setv(x, ndx, [L, R])
            # Update indices in place, since regenerating is expensive
            indices[i : i + 1] = [((*ndx, 0), L), ((*ndx, 1), R)]
            return True
    return False


def reduce(x):
    """
    >>> reduce([[[[[9,8],1],2],3],4])
    [[[[0, 9], 2], 3], 4]
    >>> reduce([7,[6,[5,[4,[3,2]]]]])
    [7, [6, [5, [7, 0]]]]
    >>> reduce([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]])
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    """
    x = deepcopy(x)

    indices = list(indexed(x))
    while _reduce_once(x, indices):
        # indices = list(indexed(x))
        pass
    return x


def add(x, y):
    """
    >>> add([[[[4,3],4],4],[7,[[8,4],9]]], [1,1])
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    >>> a = [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    >>> b = [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    >>> c = add(a, b)
    >>> c
    [[[[7, 8], [6, 6]], [[6, 0], [7, 7]]], [[[7, 8], [8, 8]], [[7, 9], [0, 6]]]]
    """
    return reduce([x, y])


def magnitude(x):
    if isinstance(x, int):
        return x
    a, b = x
    return 3 * magnitude(a) + 2 * magnitude(b)


# def magnitude(x):
#     indices = list(indexed(x))
#     depth = max(len(ndx) for (ndx, _) in indices)
#     while depth > 0:
#         pending = [
#             (i, (ndx, val))
#             for (i, (ndx, val)) in enumerate(indices)
#             if len(ndx) == depth
#         ]
#         for i, ndx, val in pending.reversed():
#             pass


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    4140
    """
    vals = [parse(x) for x in text.strip().split()]
    x = vals[0]
    for y in vals[1:]:
        x = add(x, y)
    return magnitude(x)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    3993
    """
    inputs = [parse(x) for x in text.strip().split()]
    outputs = []
    for i, x in enumerate(inputs):
        for j, y in enumerate(inputs):
            if i != j:
                outputs.append(magnitude(add(x, y)))
    return max(outputs)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
