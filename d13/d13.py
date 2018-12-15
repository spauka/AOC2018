tracks = []
trains = []

class Train:
    MOVE = {'^': (0, -1),
            'v': (0, 1),
            '<': (-1, 0),
            '>': (1, 0)}
    NEW_DIR = {('/', '<'): 'v',
               ('/', '>'): '^',
               ('/', '^'): '>',
               ('/', 'v'): '<',
               ('\\', '>'): 'v',
               ('\\', '<'): '^',
               ('\\', '^'): '<',
               ('\\', 'v'): '>'}
    DIRS = ('^', '>', 'v', '<', '^', '>', 'v', '<')

    def __init__(self, x, y, direc, turns=0, collided=False):
        self.x = x
        self.y = y
        self.direc = direc
        self.turns = turns
        self.collided = collided
    
    def __repr__(self):
        return f"Train({self.x}, {self.y}, {self.direc}, {self.turns}, {self.collided})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def move(self):
        offs = Train.MOVE[self.direc]
        return Train(self.x+offs[0], self.y+offs[1], self.direc, self.turns, self.collided)
    
    def intersect(self, int_dir):
        return Train(self.x, self.y, Train.NEW_DIR[(int_dir, self.direc)], self.turns, self.collided)
    
    def choose(self):
        new_direc = Train.DIRS[Train.DIRS.index(self.direc) + (self.turns%3 - 1)]
        return Train(self.x, self.y, new_direc, self.turns+1, self.collided)

with open("input.txt", "r") as f:
    for y, line in enumerate(f):
        if not line.strip():
            continue
        t_line = []
        for x, c in enumerate(line.strip('\n')):
            if c in ('^', 'v'):
                t_line.append('|')
                trains.append(Train(x, y, c))
            elif c in ('<', '>'):
                t_line.append('-')
                trains.append(Train(x, y, c))
            else:
                t_line.append(c)
        tracks.append(t_line)

def find_train(x, y, trains, debug=False):
    for i, train in enumerate(trains):
        if x == train.x and y == train.y and not train.collided:
            if debug:
                print(f"Found train {train}")
            return i, train
    return -1, None

def count_trains(trains):
    c = 0
    for train in trains:
        if not train.collided:
            c += 1
    return c

def print_map(tracks, trains):
    for y, line in enumerate(tracks):
        print(f"{y:4}: ", end="")
        for x, c in enumerate(line):
            _, train = find_train(x, y, trains)
            if train:
                print(train.direc, end="")
            else:
                print(c, end="")
        print()
    print()

def move_train(tracks, train):
    train = train.move()
    
    c = tracks[train.y][train.x]
    if c in ('|', '-'):
        return train
    elif c in ('/', '\\'):
        return train.intersect(c)
    elif c == '+':
        return train.choose()

def update(tracks, trains):
    trains.sort(key=lambda x: (x.y, x.x))
    for i, train in enumerate(trains):
        if train.collided:
            continue
        new_train = move_train(tracks, train)
        j, c_train = find_train(new_train.x, new_train.y, trains)
        if c_train:
            print(f"Collision with {new_train}")
            new_train.collided = True
            trains[j].collided=True
        trains[i] = new_train
    return True

#print_map(tracks, trains)
i = 0
while count_trains(trains) > 1:
    update(tracks, trains)
    #print_map(tracks, trains)
    i += 1
print(trains)
#print_map(tracks, trains)