import math
import sys

import numpy as np
from implementation import Map

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    print(len(Map(path).find_shortest_path()))
    print(len(Map(path).find_shortest_path({"a", "S"})))
