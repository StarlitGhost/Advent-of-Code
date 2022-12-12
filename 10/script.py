inputs = (line.rstrip('\n') for line in open('input'))

cycles = {'addx': 2,
          'noop': 1}

cycle = 0
instr_cycles = 0
X = 1
instr = 'noop'
operand = 0
sum_signals = 0
crt = []
for _ in range(0,6):
    crt.append(['.']*40)

def print_crt():
    for line in crt:
        print(''.join(map(str, line)))

while True:
    if instr_cycles == 0:
        if instr == 'addx':
            X += int(operand)
        try:
            instr_op = next(inputs)
            if instr_op.startswith('addx'):
                instr, operand = instr_op.split(' ')
            else:
                instr = instr_op
        except StopIteration:
            break

        instr_cycles = cycles[instr]

    instr_cycles -= 1
    cycle += 1

    if (cycle - 20) % 40 == 0:
        sum_signals += cycle * X
        print(cycle, cycle * X, sum_signals)

    crt[(cycle-1)//40][(cycle-1)%40] = '#' if X-1 <= (cycle-1)%40 <= X+1 else '.'

print_crt()
