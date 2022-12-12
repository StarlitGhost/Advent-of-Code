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
        self.encode_op()
        self.test = int(next(inputs).split(':')[1].strip().split()[-1])
        self.true = int(next(inputs).split(':')[1].strip().split()[-1])
        self.false = int(next(inputs).split(':')[1].strip().split()[-1])

        self.inspections = 0

    def encode_op(self):
        l, op, r = self.op
        if l == 'old':
            self.l = None
        else:
            self.l = int(l)
        if r == 'old':
            self.r = None
        else:
            self.r = int(r)
        ops = {'+': lambda l, r: l + r,
               '*': lambda l, r: l * r}
        self.op = ops[op]

    def inspection_worry(self, item):
        return self.op(self.l or item, self.r or item)

    def inspect_items(self, monkeys):
        for idx, item in enumerate(self.items):
            self.items[idx] = self.inspection_worry(item)
            if self.items[idx] % self.test == 0:
                target = self.true
            else:
                target = self.false
            #print(f'{self.number} -> {target} {self.items[idx]}')
            monkeys[target].items.append(self.items[idx])
            self.inspections += 1
        self.items = []

    def reduce_worry(self, mod):
        self.items = [item % mod for item in self.items]

monkeys = []
while True:
    monkeys.append(Monkey(inputs))
    print(monkeys[-1].__dict__)
    try:
        next(inputs)
    except StopIteration:
        break

mod = math.prod([monkey.test for monkey in monkeys])

for round in range(0, 10000):
    #print(f'## Round {round+1} ##')
    for monkey in monkeys:
        monkey.inspect_items(monkeys)
    #for monkey in monkeys:
    #    print(f'{monkey.number} {monkey.items}')

    for monkey in monkeys:
        monkey.reduce_worry(mod)

    if round+1 in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
        print(f'## Round {round+1} Inspections ##')
        for monkey in monkeys:
            print(f'{monkey.number} {monkey.inspections} {monkey.items}')

inspections = [monkey.inspections for monkey in monkeys]
print('Monkey Business:', math.prod(sorted(inspections)[-2:]))
