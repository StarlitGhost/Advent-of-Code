import operator

inputs = (line.rstrip('\n') for line in open('input'))

segments = []
for _ in range(0,10):
    segments.append([0,0])

dirs = {'U': (0,-1),
        'D': (0,1),
        'L': (-1,0),
        'R': (1,0)}

unique_tail_coords = set()
unique_tail_coords.add(tuple(segments[-1]))

def move_segment(head, tail):
    x = head[0]-tail[0]
    y = head[1]-tail[1]
    if x in [2,-2] and y in [2,-2]:
        tail[0] += x//2
        tail[1] += y//2
    elif x in [2,-2]:
        tail[0] += x//2
        tail[1] = head[1]
    elif y in [2,-2]:
        tail[1] += y//2
        tail[0] = head[0]
    return tail

for move in inputs:
    direction, repeat = move.split()
    d = dirs[direction]
    repeat = int(repeat)

    while repeat > 0:
        segments[0] = list(map(operator.add, segments[0], d))
        for seg in range(1, len(segments)):
            segments[seg] = move_segment(segments[seg-1], segments[seg])
        unique_tail_coords.add(tuple(segments[-1]))
        repeat -= 1
        #print(move, segments, len(unique_tail_coords))

print(len(unique_tail_coords))
