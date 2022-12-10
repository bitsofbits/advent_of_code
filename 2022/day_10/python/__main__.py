import sys

from implementation import execute, load_program, render, signal_sum

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    outputs = list(execute(load_program(path)))
    print(signal_sum(outputs))
    print(render(outputs))
