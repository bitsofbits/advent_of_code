from collections import defaultdict
from typing import NamedTuple

import numpy as np


class Particle(NamedTuple):
    ndx: int
    p: np.ndarray
    v: np.ndarray
    a: np.ndarray


def parse_chunk(chunk):
    k, x = chunk.split("=")
    x = [int(v.strip()) for v in x.strip()[1:-1].split(",")]
    return k, np.array(x)


def parse_line(i, line):
    chunks = (parse_chunk(x) for x in line.split(", "))
    return Particle(i, **{k: v for (k, v) in chunks})


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    Particle(ndx=0, p=array([3, 0, 0]), v=array([2, 0, 0]), a=array([-1,  0,  0]))
    Particle(ndx=1, p=array([4, 0, 0]), v=array([0, 0, 0]), a=array([-2,  0,  0]))
    """
    for i, line in enumerate(text.strip().split("\n")):
        yield parse_line(i, line)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    0
    """
    particles = list(parse(text))
    keys = [(abs(p.a).sum(), (p.a * p.v).sum(), p.ndx) for p in particles]
    return min(keys)[-1]


EXAMPLE2_TEXT = """
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
"""


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2
    """
    particles = list(parse(text))
    destroyed = set()
    for i in range(200):
        at_loc = defaultdict(set)
        for p in particles:
            if p.ndx in destroyed:
                continue
            at_loc[tuple(p.p)].add(p.ndx)
        for loc, indices in at_loc.items():
            if len(indices) > 1:
                for ndx in indices:
                    destroyed.add(ndx)
        for p in particles:
            p.v[:] += p.a
            p.p[:] += p.v
    return len(particles) - len(destroyed)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
