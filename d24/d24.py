from functools import total_ordering
from operator import attrgetter
import re


class Attack:
    def __init__(self, att_damage, att_type):
        self.att_damage = att_damage
        self.att_type = att_type

    def __repr__(self):
        return f"Attack({self.att_damage}, {self.att_type})"


class Group:
    _all_units = []

    def __init__(self, nunits, hp, att_damage, att_type, init):
        self.nunits = nunits
        self.hp = hp
        self.attack = Attack(att_damage, att_type)
        self.weaknesses = set()
        self.immunities = set()
        self.init = init
        self.initial_state = (nunits, att_damage, att_type)
        self._all_units.append(self)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.sort_order} {self.nunits} units>"

    def __str__(self):
        return f"<{self.__class__.__name__} group with {self.nunits} units ({self.hp} each), weak to {self.weaknesses}, immune to {self.immunities} with attack {self.attack} and initiative {self.init}>"

    @classmethod
    def all_units(cls, filter_alive=True):
        all_units = [unit for unit in cls._all_units if not filter_alive or (filter_alive and unit.alive)]
        for subclass in cls.__subclasses__():
            all_units.extend(subclass.all_units(filter_alive))
        return all_units

    @property
    def alive(self):
        return self.nunits > 0

    @property
    def effective_power(self):
        return self.nunits * self.attack.att_damage

    @property
    def sort_order(self):
        return (self.effective_power, self.init)

    def add_buff(self, btype, attribute):
        if btype == "weak":
            self.weaknesses.add(attribute)
        elif btype == "immune":
            self.immunities.add(attribute)
        else:
            raise ValueError(f"Unknown btype {btype}")

    def propose_attack(self, o):
        damage = self.attack.att_damage * self.nunits
        if self.attack.att_type in o.weaknesses:
            damage *= 2
        if self.attack.att_type in o.immunities:
            damage = 0

        return damage

    def execute_attack(self, o):
        damage = self.propose_attack(o)
        units_killed = damage // o.hp
        o.nunits -= units_killed

    def reset(self):
        self.nunits = self.initial_state[0]
        self.attack = Attack(self.initial_state[1], self.initial_state[2])


class Immune(Group):
    _all_units = []
    pass


class Infection(Group):
    _all_units = []
    pass


Immune.TARGET = Infection
Infection.TARGET = Immune


def parseInputLine(line, unitType):
    m = re.match(
        r"(\d+) units each with (\d+) hit points(?: \(([^)]+)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)", line)
    if m:
        nunits, hp, buffs, att_damage, att_type, init = m.groups()
        unit = unitType(int(nunits), int(hp), int(att_damage),
                        att_type, int(init))
        if buffs:
            buffs = parseBuffs(buffs)
            for btype, attributes in buffs:
                for attribute in attributes:
                    unit.add_buff(btype, attribute)
        return unit
    else:
        print(f"Failed {line}")


def parseBuffs(line):
    matches = re.findall(r"(\w+) to ([^;]+)*", line)
    buffs = []
    for btype, attributes in matches:
        attributes = [x.strip() for x in attributes.split(',')]
        buffs.append((btype, attributes))
    return buffs


with open("input.txt", "r") as f:
    unitType = Immune
    for line in f:
        line = line.strip()
        if not line:
            continue

        if line == "Immune System:":
            unitType = Immune
        elif line == "Infection:":
            unitType = Infection
        else:
            parseInputLine(line, unitType)

print("In Game:")
# for unit in sorted(Group.all_units(), key=attrgetter('sort_order'), reverse=True):
for unit in Group.all_units():
    print(str(unit))

def play_game(boost=False, boost_amount=0):
    # Reset all units
    for unit in Group.all_units(filter_alive=False):
        unit.reset()

    # Check if we want to boost a unit
    if boost:
        for unit in Immune.all_units():
            unit.attack.att_damage += boost_amount

    # Play Game
    while Immune.all_units() and Infection.all_units():
        # Reset targetting
        for unit in Group.all_units():
            unit.target = None
            unit.targetted = None

        # Select Targets
        for unit in sorted(Group.all_units(), key=attrgetter('sort_order'), reverse=True):
            attack_damages = []
            for target in (t for t in unit.TARGET.all_units() if not t.targetted):
                damage = unit.propose_attack(target)
                if damage > 0:
                    attack_damages.append((damage, target.sort_order, target))
            if attack_damages:
                target = max(attack_damages)[2]
                unit.target = target
                target.targetted = unit

        # Perform attacks
        pstate = sum(g.nunits for g in Group.all_units())
        for unit in sorted(Group.all_units(), key=attrgetter('init'), reverse=True):
            # Check we're not dead
            if not unit.alive or unit.target is None:
                continue
            # Otherwise execute the attack
            unit.execute_attack(unit.target)
        nstate = sum(g.nunits for g in Group.all_units())
        if pstate == nstate:
            return ("Stalemate", nstate)

    return type(Group.all_units()[0]).__name__, nstate

# Part 1
print(play_game())
print(play_game())

# Part 2
boost = 1
winner, score = play_game(True, boost)
# Double until we find a winner
while winner != 'Immune':
    print(boost, winner, score)
    boost *= 2
    winner, score = play_game(True, boost)
    if boost > 2**32 and winner == 'Stalemate':
        break
else: # Do a binary search
    lower, upper = boost//2, boost
    next_boost = lower + (upper-lower)//2

    while True:
        winner, new_score = play_game(True, next_boost)
        print(lower, next_boost, upper, winner, score)
        if winner == 'Immune':
            upper = next_boost
        elif winner == 'Infection' or winner == 'Stalemate':
            lower = next_boost
        new_next_boost = lower + (upper-lower)//2
        if new_next_boost in (lower, upper):
            print(f"Final boost: {next_boost} with score: {score}")
            break
        next_boost = new_next_boost
        score = new_score
