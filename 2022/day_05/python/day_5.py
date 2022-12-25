import sys
from collections import namedtuple

Move = namedtuple("Move", ["count", "source", "dest"])


def parse_diagram(layers):
    stacks = [[] for _ in range(9)]
    indices = [1 + 4 * i for i in range(9)]
    assert [layers[-1][i] for i in indices] == list("123456789")
    for lyr in layers[:-1]:
        for i, ndx in enumerate(indices):
            c = lyr[ndx]
            if c != " ":
                assert c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                stacks[i].append(c)
    return [x[::-1] for x in stacks]


def parse_move(txt):
    "move 3 from 2 to 1"
    _, cnt, _, src, _, dst = txt.split()
    return Move(count=int(cnt), source=int(src) - 1, dest=int(dst) - 1)


def load_inputs(path):
    with open(path) as f:
        diagram_layers = []
        for line in f:
            if not line.strip():
                break
            diagram_layers.append(line)
        moves = []
        for line in f:
            if line.strip():
                moves.append(parse_move(line))
    return parse_diagram(diagram_layers), moves


def apply_moves_cm9000(stacks, moves):
    for m in moves:
        for _ in range(m.count):
            stacks[m.dest].append(stacks[m.source].pop())


def apply_moves_cm9001(stacks, moves):
    for m in moves:
        crates = stacks[m.source][-m.count :]
        del stacks[m.source][-m.count :]
        stacks[m.dest].extend(crates)


if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    stacks, moves = load_inputs(path)
    apply_moves_cm9000(stacks, moves)
    print("".join(x[-1] for x in stacks))

    stacks, moves = load_inputs(path)
    apply_moves_cm9001(stacks, moves)
    print("".join(x[-1] for x in stacks))
