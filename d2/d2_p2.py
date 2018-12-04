with open("input.txt", "r") as inputFile:
    ids = tuple(line.strip() for line in inputFile if line.strip())

for i, id1 in enumerate(ids):
    for id2 in ids[1:]:
        count = sum(int(c1 != c2) for c1, c2 in zip(id1, id2))
        if count == 1:
            print("Characters are: ", end='')
            for c1, c2 in zip(id1, id2):
                if c1 == c2:
                    print(c1, end='')
            print('')
