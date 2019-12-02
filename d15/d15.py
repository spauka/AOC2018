from functools import total_ordering
from collections import defaultdict, deque, namedtuple

Nodes = namedtuple("Nodes", ("dist", "pos", "previous"))
Action = namedtuple("Action", ("action", "creature", "pos"))

@total_ordering
class Creature:
    def __init__(self, x, y, grid):
        self.hp = 200
        self.x = x
        self.y = y
        self.grid = grid
        self.alive = True

    def __repr__(self):
        return f"<{self.__class__.__name__} @ {self.pos}, HP: {self.hp}>"

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
    @pos.setter
    def pos(self, newpos):
        self.x, self.y = newpos
    @property
    def c(self):
        return "C"
    @property
    def power(self):
        return 3

    def is_target(self, o):
        raise NotImplementedError("Should be implemented in a real creature")

    def pick_next_action(self):
        # Find targets and check if any are in range
        targets = {}
        near_targets = []

        # Check if there are any creatures in range, and calculate
        # where we'd move if there is one
        targets_avail = False
        for t in self.grid.alive:
            if not self.is_target(t):
                continue
            targets_avail = True
            if self.pos in t.hitbox():
                near_targets.append(t)
            for target in t.target_area():
                if target not in targets:
                    targets[target] = t
        if not targets_avail:
            return Action("game_end", None, self.pos)

        if near_targets:
            near_targets.sort(key=lambda x: (x.hp, x))
            return Action("target", near_targets[0], self.pos)

        # If we've gotten here, we need to move, let's figure out
        # where to move.
        d_grid = self.grid.calc_d(self.pos)
        # Figure out the nearest targets
        mins = []
        minv = float('inf')
        for t in targets:
            if t in d_grid:
                if d_grid[t].dist < minv:
                    minv = d_grid[t].dist
                    mins = [t]
                elif d_grid[t].dist == minv:
                    mins.append(t)

        if mins:
            mins.sort(key=lambda x: (x[1], x[0]))
            path = self.grid.backtrack(d_grid[mins[0]])
            return Action("move", self, path[1].pos)
        else:
            return Action("none", self, None)

    def hitbox(self):
        return self.grid.neighbours_valid(self.pos)
    def target_area(self):
        return self.grid.neighbours_empty(self.pos)

class Elf(Creature):
    POWER = 3

    @property
    def c(self):
        return "E"

    def is_target(self, o):
        return isinstance(o, Goblin)

    @property
    def power(self):
        return self.POWER

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

    def neighbours(self, pos):
        possibilities = ((pos[0],   pos[1]-1),
                         (pos[0]-1, pos[1]),
                         (pos[0]+1, pos[1]),
                         (pos[0],   pos[1]+1))
        return possibilities
    def neighbours_valid(self, pos):
        return tuple(p for p in self.neighbours(pos) if self.validate_pos(p))
    def neighbours_empty(self, pos):
        return tuple(p for p in self.neighbours_valid(pos) if self.at_pos(p) is None)

    @property
    def alive(self):
        return tuple(c for c in self.creatures if c.alive)

    def validate_pos(self, pos):
        if pos[0] < 0 or pos[0] >= self.xdim:
            return False
        if pos[1] < 0 or pos[1] >= self.ydim:
            return False
        if self[pos] == "#":
            return False
        return True
    def at_pos(self, pos):
        for c in self.alive:
            if pos == c.pos:
                return c
        return None

    def calc_d(self, pos):
        visited = {}
        next_nodes = deque((Nodes(0, pos, None),))
        at_pos = {c.pos for c in self.alive}

        while next_nodes:
            visiting = next_nodes.pop()
            for neighbour in self.neighbours_valid(visiting.pos):
                if neighbour in visited or neighbour in at_pos:
                    continue
                new_node = Nodes(visiting.dist+1, neighbour, visiting)
                visited[neighbour] = new_node
                next_nodes.appendleft(new_node)
        return visited
    def backtrack(self, end):
        path = deque()
        while end:
            path.appendleft(end)
            end = end.previous
        return tuple(path)

    def print_grid(self, flag=()):
        for y, l in enumerate(self.grid):
            for x, c in enumerate(l):
                creature = self.at_pos((x, y))
                if (x, y) in flag and creature is not None:
                    print(creature.c.lower(), end="")
                elif creature is not None:
                    print(creature.c, end="")
                elif (x, y) in flag:
                    print('!', end="")
                else:
                    print(c, end="")
            print()
    def print_dist_grid(self, dists):
        for y, l in enumerate(self.grid):
            for x, c in enumerate(l):
                if (x, y) in dists:
                    print(f"{dists[(x, y)].dist:<3}", end="")
                else:
                    print(f"{c:3}", end="")
            print()

    @property
    def xdim(self):
        return len(self.grid[0])
    @property
    def ydim(self):
        return len(self.grid)

def solve(elf_power=3):
    grid = Grid()
    with open("input.txt", "r") as f:
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

    Elf.POWER = elf_power

    rounds = 0
    while True:
        for c in grid.alive:
            if not c.alive: # Could have died during the turn...
                continue
            action = c.pick_next_action()

            # Check if the game is over
            if action.action == "game_end":
                break

            # Check if we need to move
            if action.action == "move":
                c.pos = action.pos
                action = c.pick_next_action()
            if action.action == "target":
                action.creature.hp -= c.power
                if action.creature.hp <= 0:
                    action.creature.alive = False
        else:
            grid.creatures.sort()
            rounds += 1
            continue
        break

    print(f"Game over after {rounds} rounds. Creatures alive: {grid.alive}.")

    points = sum(c.hp for c in grid.alive)*rounds

    print(f"Score: {points}")
    return all(tuple(c.alive for c in grid.creatures if isinstance(c, Elf)))

power = 3
all_alive = solve(power)
while not all_alive:
    power += 1
    print(f"Solving with power {power}")
    all_alive = solve(power)