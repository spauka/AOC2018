import re
from collections import defaultdict
from functools import partial
import numpy as np

def qp(line):
    m = re.findall(r"(\d+)", line)
    return tuple(int(x) for x in m)

with open("input.txt", "r") as inp:
    for line in inp:
        if not line:
            continue
        _ = qp(line)