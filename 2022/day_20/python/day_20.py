import sys
from time import perf_counter

from implementation import coord_sum, decrypt, mix, parse_text

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    t0 = perf_counter()
    q = coord_sum(mix(parse_text(text)))  # 8721
    print(f"Part 1: coord sum mix: {q} ({perf_counter() - t0:.0f}s)")

    t0 = perf_counter()
    q = coord_sum(decrypt(parse_text(text)))  # 831878881825
    print(f"Part 2: coord sum decrypt: {q} ({perf_counter() - t0:.0f}s)")
