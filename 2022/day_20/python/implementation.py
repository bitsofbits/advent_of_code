from collections import deque

example_text = """
1
2
-3
3
-2
0
4
"""


def parse_text(text):
    """
    >>> parse_text(example_text)
    [1, 2, -3, 3, -2, 0, 4]
    """
    return [int(x.strip()) for x in text.strip().split()]


def shift(i, numbers):
    _, n = numbers[i]
    if n != 0:
        N = len(numbers) - 1
        x = numbers.pop(i)
        j = (i + n) % N
        numbers.insert(j, x)


def equiv(x, y):
    """x and y are the same within a rotation"""
    if x == y:
        return True
    x = deque(x)
    y = deque(y)
    for i in range(len(x) - 1):
        y.rotate(1)
        if x == y:
            return True
    return False


def mix(numbers, n=1):
    """
    >>> numbers = parse_text(example_text)
    >>> equiv(mix(numbers), [1, 2, -3, 4, 0, 3, -2])
    True
    """
    numbers = deque(enumerate(numbers))
    N = len(numbers) - 1
    for _ in range(n):
        for i0 in range(len(numbers)):
            # Ugh N**2 performance here. Could track this with another
            # lookup table, but indexing would be a headache and this i
            # fast enough,
            for j, (i1, n) in enumerate(numbers):
                if i0 == i1:
                    break
            if n != 0:
                numbers.rotate(-j)
                x = numbers.popleft()
                numbers.insert(n % N, x)
    return [x for (_, x) in numbers]


def coord_sum(numbers):
    """
    >>> coord_sum(mix(parse_text(example_text)))
    3
    """
    n = len(numbers)
    i0 = numbers.index(0)
    coords = [numbers[(i0 + 1000 * (i + 1)) % n] for i in range(3)]
    return sum(coords)


def decrypt(numbers):
    """
    >>> coord_sum(decrypt(parse_text(example_text)))
    1623178306
    """
    key = 811589153
    numbers = [x * key for x in numbers]
    numbers = mix(numbers, 10)
    return numbers


if __name__ == "__main__":
    import doctest

    doctest.testmod()
