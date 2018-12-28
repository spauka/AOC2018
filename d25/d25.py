import re

def qp(line):
    m = re.findall(r"([-\d]+)", line)
    return tuple(int(x) for x in m)

class Pos:
    __slots__ = ['x', 'y', 'z', 't']
    def __init__(self, x, y, z, t):
        self.x = x
        self.y = y
        self.z = z
        self.t = t
    
    def __repr__(self):
        return f"Pos({self.x}, {self.y}, {self.z})"

    def __add__(self, o):
        return Pos(self.x+o.x, self.y+o.y, self.z+o.z, self.t+o.t)
    def __sub__(self, o):
        return Pos(self.x-o.x, self.y-o.y, self.z-o.z, self.t+o.t)
    
    def dist(self, o):
        return sum(abs(d) for d in (self.x-o.x, self.y-o.y, self.z-o.z, self.t-o.t))

class Constellation(list):
    def check_point(self, o):
        for p in self:
            if p.dist(o) <= 3:
                return True
        return False

    def check_merge(self, o):
        for p in o:
            if self.check_point(p):
                return True
        return False

constellations = []
with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        p = Pos(*qp(line))

        # Check if this belongs in any constallations
        for c in constellations:
            if c.check_point(p):
                c.append(p)
                break
        else:
            constellations.append(Constellation((p,)))

pnconst = 0
nconst = len(constellations)
while nconst != pnconst:
    pnconst = nconst
    i = 0
    while i < nconst:
        j = i+1
        while j < nconst:
            if constellations[i].check_merge(constellations[j]):
                constellations[i].extend(constellations[j])
                constellations.pop(j)
                nconst -= 1
            else:
                j += 1
        i += 1
    print(f"{pnconst:5} -> {nconst:5}")
