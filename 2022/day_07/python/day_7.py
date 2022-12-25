import bisect
import sys


def process_cmd(line, path):
    assert line.startswith("$ "), line
    line = line[2:].strip()
    if line == "ls":
        return "ls", path, True
    else:
        cmd, arg = line.split()
        if cmd == "cd":
            if arg == "/":
                path = [arg]
            elif arg == "..":
                path.pop()
            else:
                assert "/" not in arg, line
                path.append(arg)
            return "cd", path, False
        else:
            raise ValueError(f"bad command {line}")


def process_listing(line):
    size, name = line.strip().split()
    if size != "dir":
        size = int(size)
    return (name, size)


def process_commands(filepath):
    path = None
    expect_data = False
    dirs = {}
    with open(filepath) as f:
        for line in f:
            if line.startswith("$"):
                cmd, path, expect_data = process_cmd(line, path)
            else:
                assert expect_data
                key = "/".join(path)
                if key not in dirs:
                    dirs[key] = []
                dirs[key].append(process_listing(line))
    return dirs


def find_size(path, dirs):
    size = 0
    for name, sz in dirs[path]:
        if sz == "dir":
            subpath = f"{path}/{name}"
            sz = find_size(subpath, dirs)
        size += sz
    return size


if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    dirs = process_commands(path)
    sizes = {k: find_size(k, dirs) for k in dirs}
    total_small = sum(v for v in sizes.values() if v <= 100000)
    print(total_small)

    total_space = 70000000
    needed = 30000000
    must_delete = needed - (total_space - sizes["/"])

    keys = sorted(sizes, key=lambda x: sizes[x])
    values = [sizes[k] for k in keys]
    ndx = bisect.bisect_left(values, must_delete)
    print(values[ndx])
