import math
import sys

import numpy as np
from implementation import Map

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    print(len(Map(path).find_traverse()))

    # n =
    # # candidates = []
    # # dist = math.inf
    # # for i in range(map_.shape[0]):
    # #     for j in range(map_.shape[1]):
    # #         if map_.rows[i][j] == "a":
    # #             steps = map_.find_traverse((i, j))
    # #             if not steps or steps[-1] != map_.end:
    # #                 continue
    # #             n = len(steps)
    # #             if n < dist:
    # #                 dist = n
    # print(i, j, dist)
    print(Map(path).find_shortest_from({"a", "S"}))
