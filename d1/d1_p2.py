from operator import add, sub
from itertools import cycle

OP = {'+': add, '-': sub}

def tokenize(inp):
    for line in inp:
        if line:
            yield (OP[line[0]], int(line[1:]))

offset = 0
seen = set()

with open("input.txt", "r") as inputFile:
    for op, change in cycle(tokenize(inputFile)):
        offset = op(offset, change)
        if offset in seen:
            print(f"Frequency {offset} seen twice")
            break
        seen.add(offset)
