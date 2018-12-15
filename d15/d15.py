from itertools import product
from operator import attrgetter
from functools import total_ordering

@total_ordering
class Creature:
    def __init__(self, x, y, grid):
        self.hp = 200
        self.x = x
        self.y = y
        self.grid = grid
    
    def __repr__(self):
        return f"<{self.__class__.__name__} @ ({self.x}, {self.y}), HP: {self.hp}>"

    def __eq__(self, o):
        if not isinstance(o, self.__class__):
            return False
        if self.x == o.x and self.y == o.y:
            return True
        return False
    def __lt__(self, o):
        return (self.y, self.x) < (o.y, o.x)

    @property
    def pos(self):
        return (self.x, self.y)
    @property
    def c(self):
        return "C"

    def hitbox(self):
        possibilities = ((self.x-1, self.y), 
                         (self.x, self.y-1),
                         (self.x+1, self.y),
                         (self.x, self.y+1))
        return set(p for p in possibilities if self.grid.validate_pos(p))
    
    def path_to(self, pos):
        visited = set()

class Elf(Creature):
    @property
    def c(self):
        return "E"

    def is_target(self, o):
        return isinstance(o, Goblin)

class Goblin(Creature):
    @property
    def c(self):
        return "G"
    
    def is_target(self, o):
        return isinstance(o, Elf)

class Grid:
    def __init__(self):
        self.grid = []
        self.creatures = []
    
    def __repr__(self):
        return f"<Grid({self.xdim}, {self.ydim})>"

    def __getitem__(self, pos):
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise TypeError("pos must be a tuple, with format (x,y)")
        return self.grid[pos[1]][pos[0]]

    def append(self, line):
        line = tuple(line)
        if self.grid:
            if len(line) != self.xdim:
                raise ValueError("Line must be the same length as other lines")
        self.grid.append(line)
    def append_creature(self, ctype, pos):
        if not isinstance(ctype, type) and issubclass(ctype, Creature):
            raise TypeError("ctype must be a type of creature")
        self.creatures.append(ctype(*pos, self))
        self.creatures.sort()

    def validate_pos(self, pos):
        if pos[0] < 0 or pos[0] >= self.xdim:
            return False
        if pos[1] < 0 or pos[1] >= self.ydim:
            return False
        if self[pos] == "#":
            return False
        return True

    def at_pos(self, pos):
        for c in self.creatures:
            if pos == c.pos:
                return c
        return None

    def print_grid(self, flag=()):
        for y, l in enumerate(self.grid):
            for x, c in enumerate(l):
                creature = self.at_pos((x, y))
                if creature is not None:
                    print(creature.c, end="")
                elif (x, y) in flag:
                    print('!', end="")
                else:
                    print(c, end="")
            print()
    
    @property
    def xdim(self):
        return len(self.grid[0])
    @property
    def ydim(self):
        return len(self.grid)

grid = Grid()
with open("input_s.txt", "r") as f:
    for y, line in enumerate(f):
        line = line.strip()
        cline = []
        for x, c in enumerate(line):
            if c == "E":
                grid.append_creature(Elf, (x, y))
                cline.append('.')
            elif c == "G":
                grid.append_creature(Goblin, (x, y))
                cline.append('.')
            else:
                cline.append(c)
        grid.append(tuple(cline))

grid.print_grid()
for c in grid.creatures:
    print(f"Targets for creature {c}")
    targets = set()
    for t in grid.creatures:
        if c.is_target(t):
            targets = targets.union(t.hitbox())
    grid.print_grid(targets)
print(grid.creatures)