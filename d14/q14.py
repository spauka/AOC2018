recipes = [3, 7]

elf1 = 0
elf2 = 1

rounds = "635041"
match = tuple(int(x) for x in str(rounds))

def print_list(l, elves):
    for i, x in enumerate(l):
        if i in elves:
            print(f"({x})", end="")
        else:
            print(f" {x} ", end="")
    print()

while True:
    ns = recipes[elf1] + recipes[elf2]
    digits = list(int(x) for x in str(ns))
    recipes.extend(digits)
    elf1 = (elf1 + recipes[elf1] + 1)%len(recipes)
    elf2 = (elf2 + recipes[elf2] + 1)%len(recipes)

    if match == tuple(recipes[-len(match):]):
        print(len(recipes)-len(match))
        break
    if len(digits) == 2:
        if match == tuple(recipes[-len(match)-1:-1]):
            print(len(recipes)-len(match)-1)
            break
    #print_list(recipes, (elf1, elf2))
