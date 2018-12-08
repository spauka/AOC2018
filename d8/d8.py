import re
from collections import defaultdict
from functools import partial
import numpy as np

def qp(line):
    m = re.findall(r"(\d+)", line)
    return tuple(int(x) for x in m)

lines = []
with open("input.txt", "r") as inp:
    for line in inp:
        if not line:
            continue
        lines.append(qp(line))

assert len(lines) == 1
line = lines[0]

def parse_tree(l, start_ind):
    num_nodes, num_metadata = l[start_ind:start_ind+2]

    c_nodes = []
    metadata = None
    metadata_csum = 0

    start_ind += 2
    for i in range(num_nodes):
        child, start_ind, metadata_sum, chcksum = parse_tree(l, start_ind)
        metadata_csum += metadata_sum
        c_nodes.append((child, metadata_sum, chcksum))
    c_nodes = tuple(c_nodes)
    metadata = l[start_ind:start_ind+num_metadata]
    metadata_csum += sum(metadata)

    checksum = 0
    if num_nodes:
        for m in metadata:
            if m == 0:
                continue
            if m > len(c_nodes):
                continue
            checksum += c_nodes[m-1][2]
    else:
        checksum = sum(metadata)

    return c_nodes, start_ind+num_metadata, metadata_csum, checksum

tree, _, csum, chksum = parse_tree(line, 0)
print(f"Part 1: {csum}")
print(f"Part 2: {chksum}")

