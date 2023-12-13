import sys
from pprint import pprint

def find_mirror(map_):
    for i in range(1, len(map_)):
        if map_[i] == map_[i-1]:
            #print(f'{i}:{i+1}')
            for j in range(1,len(map_)):
                #print(f'{i+j+1}-{i-1-j+1}')
                if i+j >= len(map_) or i-1-j < 0:
                    return i
                if map_[i+j] != map_[i-1-j]:
                    break
    return 0

if __name__ == '__main__':
    maps = open(sys.argv[1] if len(sys.argv) > 1 else '13/input').read().strip().split('\n\n')

    total = 0
    for i, m in enumerate(maps):
        m = [[c for c in row] for row in m.split('\n')]
        #print(f'map {i}:')
        row = find_mirror(m)
        total += row*100
        #print(row)
        col = find_mirror(list(zip(*m)))
        total += col
        #print(col)
        if row == 0 and col == 0:
            print('\n'.join(''.join(row) for row in m))
    print(total)
