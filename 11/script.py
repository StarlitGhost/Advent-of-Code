import sys
import math

if len(sys.argv) < 2:
    print('missing input filename')
    exit()

inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

class Monkey:
    def __init__(self, inputs):
        self.number = int(next(inputs).split()[1][0:-1])
        self.items = list(map(int, next(inputs).split(':')[1].strip().split(', ')))
        self.op = next(inputs).split(':')[1].strip().split(' = ')[1].split()
        self.test = int(next(inputs).split(':')[1].strip().split()[-1])
        self.true = int(next(inputs).split(':')[1].strip().split()[-1])
        self.false = int(next(inputs).split(':')[1].strip().split()[-1])

        self.inspections = 0

    def inspection_worry(self, item):
        l, op, r = self.op
        if l == 'old':
            l = item
        else:
            l = int(l)
        if r == 'old':
            r = item
        else:
            r = int(r)
        ops = {'+': lambda l, r: l + r,
               '*': lambda l, r: l * r}
        #print(' '.join(self.op), '=', l, op, r, '=', ops[op](l, r))
        return ops[op](l, r)

    def inspect_items(self, monkeys):
        for idx, item in enumerate(self.items):
            self.items[idx] = self.inspection_worry(item)
            self.items[idx] //= 3
            if self.items[idx] % self.test == 0:
                target = self.true
            else:
                target = self.false
            #print(f'{self.number} -> {target} {self.items[idx]}')
            monkeys[target].items.append(self.items[idx])
            self.inspections += 1
        self.items = []

monkeys = []
while True:
    monkeys.append(Monkey(inputs))
    print(monkeys[-1].__dict__)
    try:
        next(inputs)
    except StopIteration:
        break

for round in range(0, 20):
    print(f'## Round {round+1} ##')
    for monkey in monkeys:
        monkey.inspect_items(monkeys)
    for monkey in monkeys:
        print(f'{monkey.number} {monkey.items}')

print('## Inspections ##')
for monkey in monkeys:
    print(f'{monkey.number} {monkey.inspections}')

inspections = [monkey.inspections for monkey in monkeys]
print('Monkey Business:', math.prod(sorted(inspections)[-2:]))
