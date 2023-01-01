from ast import literal_eval

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


def emit_indexed(val):
    """
    >>> list(emit_indexed([[1,2],3]))
    [((0, 0), 1), ((0, 1), 2), ((1,), 3)]
    """
    stack = [(val, (), 0)]
    while stack:
        x, ndx, depth = stack.pop()
        if isinstance(x, int):
            yield ndx, x, depth
        else:
            L, R = x
            stack.append((R, (*ndx, 1), depth + 1))
            stack.append((L, (*ndx, 0), depth + 1))


def indexed(val):
    return list(emit_indexed(val))


def indices_of(val):
    """
    >>> list(indices_of([[1,2],3]))
    [(0, 0), (0, 1), (1,)]
    """
    for (ndx, x, d) in indexed(val):
        yield ndx


def _reduce_once(indices):
    # First check if we need to explode anything
    for i, (ndx, val, depth) in enumerate(indices):
        if depth == 5:
            lval = val
            _, rval, _ = indices[i + 1]
            if i - 1 >= 0:
                ndx_n, nval, depth_n = indices[i - 1]
                nval += lval
                indices[i - 1] = (ndx_n, nval, depth_n)
            if i + 2 < len(indices):
                ndx_p, pval, depth_p = indices[i + 2]
                pval += rval
                indices[i + 2] = (ndx_p, pval, depth_p)
            indices[i : i + 2] = [(ndx[:-1], 0, depth - 1)]
            return True
    # Then if we need to split anything
    for i, (ndx, v, depth) in enumerate(indices):
        if v >= 10:
            L = v // 2
            R = v - L
            indices[i : i + 1] = [((*ndx, 0), L, depth + 1), ((*ndx, 1), R, depth + 1)]
            return True
    return False


def reduce(indices):
    while _reduce_once(indices):
        pass
    return indices


def add(ndx_a, ndx_b):
    """
    >>> a = [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    >>> b = [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    >>> c = add(indexed(a), indexed(b))
    >>> magnitude(c)
    3993
    """
    ndx_a = [((0, *ndx), v, d + 1) for (ndx, v, d) in ndx_a]
    ndx_b = [((1, *ndx), v, d + 1) for (ndx, v, d) in ndx_b]
    return reduce(ndx_a + ndx_b)


def magnitude(indices):
    indices = indices.copy()
    depth = max(depth for (ndx, val, depth) in indices)
    while depth > 0:
        pending = [
            (i, (ndx, val, d))
            for (i, (ndx, val, d)) in enumerate(indices)
            if d == depth
        ][::-1]
        assert len(pending) % 2 == 0
        for j in range(0, len(pending), 2):
            i0, (ndx0, val0, d0) = pending[j + 1]
            i1, (ndx1, val1, d1) = pending[j]
            v = 3 * val0 + 2 * val1
            indices[i0 : i0 + 2] = [(ndx0[:-1], v, d0 - 1)]
        depth -= 1
    [(_, mag, _)] = indices
    return mag


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    4140
    """
    vals = [indexed(parse(x)) for x in text.strip().split()]
    x = vals[0]
    for y in vals[1:]:
        x = add(x, y)
    return magnitude(x)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    3993
    """
    inputs = [indexed(parse(x)) for x in text.strip().split()]
    outputs = []
    for i, x in enumerate(inputs):
        for j, y in enumerate(inputs):
            if i != j:
                outputs.append(magnitude(add(x, y)))
    return max(outputs)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
