import sys
from pprint import pprint

mapStore = {}

def hamming_distance(left, right):
    return sum(l != r for l, r in zip(left, right))

def find_mirror(map_, smudges=False, mapIndex=0, row_col='row'):
    for i in range(1, len(map_)):
        diff = hamming_distance(map_[i], map_[i-1])
        if diff == 0 or (smudges and diff == 1):
            if smudges:
                smudge_count = diff
            for j in range(1,len(map_)):
                if i+j >= len(map_) or i-1-j < 0:
                    if smudges and i == mapStore[mapIndex][row_col]:
                        # we found the same row/col without smudges, skip it
                        break
                    else:
                        return i
                if map_[i+j] != map_[i-1-j]:
                    if smudges and hamming_distance(map_[i+j], map_[i-1-j]) == 1:
                        smudge_count += 1
                        if smudge_count > 1:
                            # too many smudges needed for this to be the mirror, skip
                            break
                        continue
                    break
    return 0

if __name__ == '__main__':
    maps = open(sys.argv[1]).read().strip().split('\n\n')

    total = 0
    totals = 0
    for i, m in enumerate(maps):
        m = [[c for c in row] for row in m.split('\n')]

        row = find_mirror(m)
        # store the row so we can tell if the smudge changes it
        mapStore[i] = {'row': row}
        rows = find_mirror(m, True, i, 'row')
        total += row*100
        totals += rows*100

        col = find_mirror(list(zip(*m)))
        # store the col so we can tell if the smudge changes it
        mapStore[i]['col'] = col
        cols = find_mirror(list(zip(*m)), True, i, 'col')
        total += col
        totals += cols

        # print maps where we don't find reflection lines, for debug
        if row == 0 and col == 0:
            print(f'map {i}:')
            print('\n'.join(''.join(row) for row in m))
        if rows == 0 and cols == 0:
            print(f'smudged map {i}:')
            print('\n'.join(''.join(row) for row in m))
    print(total)
    print(totals)
