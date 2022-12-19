import sys
from time import perf_counter

from implementation import (compute_geode_product, compute_total_quality,
                            load_blueprints)

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    blueprints = load_blueprints(path)

    t0 = perf_counter()
    q = compute_total_quality(blueprints)
    print(f"Part 1: total quality: {q} ({perf_counter() - t0:.0f}s)")

    t0 = perf_counter()
    p = compute_geode_product(blueprints)
    print(f"Part 2: geode product: {p} ({perf_counter() - t0:.0f}s")
