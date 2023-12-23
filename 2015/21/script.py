import sys
import itertools

shop_text = """Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
Nothing       0     0       0

Rings:      Cost  Damage  Armor
Damage_+1    25     1       0
Damage_+2    50     2       0
Damage_+3   100     3       0
Defense_+1   20     0       1
Defense_+2   40     0       2
Defense_+3   80     0       3
Nothing_1     0     0       0
Nothing_2     0     0       0"""

shop = {}
for section in shop_text.split('\n\n'):
    section = section.split('\n')
    section_name = section[0].split()[0].rstrip(':')
    shop[section_name] = []
    for item in section[1:]:
        props = ['name','cost','dmg','arm']
        shop[section_name].append({pair[0]: pair[1] for pair in zip(props, item.split())})
        for prop in props[1:]:
            shop[section_name][-1][prop] = int(shop[section_name][-1][prop])

def fight(gear, boss):
    p_hp = 100
    cost = sum(slot['cost'] for slot in gear)
    dmg = sum(slot['dmg'] for slot in gear)
    arm = sum(slot['arm'] for slot in gear)

    p_dmg = max(1, dmg - boss['arm'])
    b_dmg = max(1, boss['dmg'] - arm)
    b_hp = boss['hp']

    while True:
        b_hp -= p_dmg
        if b_hp <= 0:
            return True, cost
        p_hp -= b_dmg
        if p_hp <= 0:
            return False, cost


if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]
    boss = {'hp': int(inputs[0].split(': ')[1]),
            'dmg': int(inputs[1].split(': ')[1]),
            'arm': int(inputs[2].split(': ')[1])}

    min_cost = 1000
    min_gear = []
    max_cost = 0
    max_gear = []

    for wep in shop['Weapons']:
        for arm in shop['Armor']:
            for r1, r2 in itertools.combinations(shop['Rings'], 2):
                gear = [wep, arm, r1, r2]
                win, cost = fight(gear, boss)
                if win and cost < min_cost:
                    min_cost = cost
                    min_gear = gear
                if not win and cost > max_cost:
                    max_cost = cost
                    max_gear = gear

    print(min_cost, [gear['name'] for gear in min_gear])
    print(max_cost, [gear['name'] for gear in max_gear])
