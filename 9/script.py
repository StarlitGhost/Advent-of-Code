import operator

inputs = (line.rstrip('\n') for line in open('input'))

head = [0,0]
tail = [0,0]

dirs = {'U': (0,-1),
        'D': (0,1),
        'L': (-1,0),
        'R': (1,0)}

unique_tail_coords = set()
unique_tail_coords.add(tuple(tail))

for move in inputs:
    direction, repeat = move.split()
    d = dirs[direction]
    repeat = int(repeat)

    while repeat > 0:
        head = list(map(operator.add, head, d))
        x = head[0]-tail[0]
        y = head[1]-tail[1]
        if x in [2,-2]:
            tail[0] += x//2
            tail[1] = head[1]
        if y in [2,-2]:
            tail[1] += y//2
            tail[0] = head[0]
        unique_tail_coords.add(tuple(tail))
        repeat -= 1

    print(move, head, tail, len(unique_tail_coords))
