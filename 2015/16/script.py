import sys
import re


wrapping = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

def check_sue_p1(sue):
    for prop, amount in sue.items():
        if amount != wrapping[prop]:
            return False
    return True

def check_sue_p2(sue):
    for prop, amount in sue.items():
        if prop in ['cats', 'trees']:
            if amount <= wrapping[prop]:
                return False
        elif prop in ['pomeranians', 'goldfish']:
            if amount >= wrapping[prop]:
                return False
        elif wrapping[prop] != amount:
            return False
    return True


if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))
    
    sues = {}
    for i, line in enumerate(inputs):
        sues[i+1] = {name: int(amount) for name, amount in map(lambda s: s.split(': '), re.sub(r'^Sue \d+: ', '', line).split(', '))}

    for number, sue in sues.items():
        if check_sue_p1(sue):
            print('p1', number, sue)
        if check_sue_p2(sue):
            print('p2', number, sue)
