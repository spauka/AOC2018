import string

with open("input.txt", "r") as inp:
    inp_poly = inp.read().strip()
    
def react(polymer):
    polymer = polymer.encode('ASCII')

    new_string = []
    for c1 in polymer:
        if not new_string:
            new_string.append(c1)
            continue
        
        c2 = new_string[-1]
        c1_lower = c1 if c1 >= 97 else c1+32
        c2_lower = c2 if c2 >= 97 else c2+32
        if c1 != c2 and c1_lower == c2_lower:
            new_string.pop()
        else:
            new_string.append(c1)
    return len(new_string)

print(f"Size is: {react(inp_poly)}")

repl = []
for i, char in enumerate(string.ascii_lowercase):
    rep_poly = inp_poly.replace(char, '').replace(char.upper(), '')
    repl.append(react(rep_poly))

output = sorted(zip(repl, string.ascii_lowercase))
print(f"remove {output[0][1]} to get length {output[0][0]}")