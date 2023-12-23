from GhostyUtils import aoc
from GhostyUtils.diff import hamming_distance
from GhostyUtils.grid import Grid

mapStore = {}


def find_mirror(map_, smudges=False, mapIndex=0, row_col='row'):
    for i in range(1, map_.height()):
        diff = hamming_distance(map_[i], map_[i-1])
        if diff == 0 or (smudges and diff == 1):
            if smudges:
                smudge_count = diff
            for j in range(1, map_.height()):
                if i+j >= map_.height() or i-1-j < 0:
                    # reached the edge of the map
                    if smudges and i == mapStore[mapIndex][row_col]:
                        # we found the same row/col without smudges, skip it
                        break
                    else:
                        return i

                # compare row/col pairs outward from our current position
                diff = hamming_distance(map_[i+j], map_[i-1-j])
                if diff == 0 or (smudges and diff == 1):
                    if diff == 1:
                        smudge_count += 1
                        if smudge_count > 1:
                            # too many smudges for this to be the mirror, skip
                            break
                    continue
                else:
                    break
    return 0


if __name__ == '__main__':
    maps = aoc.read_sections()

    total = 0
    totals = 0
    for i, m in enumerate(maps):
        m = Grid(m.split('\n'))

        row = find_mirror(m)
        # store the row so we can tell if the smudge changes it
        mapStore[i] = {'row': row}
        rows = find_mirror(m, True, i, 'row')
        total += row*100
        totals += rows*100

        col = find_mirror(m.transposed())
        # store the col so we can tell if the smudge changes it
        mapStore[i]['col'] = col
        cols = find_mirror(m.transposed(), True, i, 'col')
        total += col
        totals += cols

        # print maps where we don't find reflection lines, for debug
        if row == 0 and col == 0:
            print(f'map {i}:')
            print(m)
        if rows == 0 and cols == 0:
            print(f'smudged map {i}:')
            print(m)

    print(total)
    print(totals)
