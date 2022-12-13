import sys

from implementation import Rope, find_n_tail_locs, load_moves

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    moves = load_moves(path)
    print(find_n_tail_locs(Rope(2), moves))
    print(find_n_tail_locs(Rope(10), moves))
