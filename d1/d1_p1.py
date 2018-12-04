from operator import add, sub

OP = {'+': add, '-': sub}

def tokenize(inp):
    for line in inp:
        if line:
            yield (OP[line[0]], int(line[1:]))

with open("input.txt", "r") as inputFile:
    offset = 0
    for op, change in tokenize(inputFile):
        offset = op(offset, change)
    print(f"Offset was: {offset}")
