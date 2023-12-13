import sys
import itertools
from GhostyUtils.vec2 import manhattan_distance
from GhostyUtils.grid import Grid

def mh_distance_expanded(start, end, rows, cols, expansion):
    dist = manhattan_distance(start, end)
    s = start
    e = end
    for col in cols:
        if (s.x < e.x and s.x < col < e.x) or (e.x < s.x and e.x < col < s.x):
            dist += expansion
    for row in rows:
        if (s.y < e.y and s.y < row < e.y) or (e.y < s.y and e.y < row < s.y):
            dist += expansion
    return dist

def expansion_rows_cols(grid):
    expand_rows = [y for y, row in enumerate(grid.by_rows()) if all(x == '.' for x in row)]
    expand_columns = [x for x, col in enumerate(grid.by_cols()) if all(y == '.' for y in col)]
    return expand_rows, expand_columns

def find_distances_expanded(galaxies, rows, cols, expansion):
    distances = [mh_distance_expanded(pair[0], pair[1], rows, cols, expansion)
                 for pair in itertools.combinations(galaxies, 2)]
    return distances

if __name__ == '__main__':
    inputs = open(sys.argv[1]).read().strip().split('\n')
    space = Grid(inputs)

    rows, cols = expansion_rows_cols(space)
    galaxies = list(space.find_all('#'))

    distances = find_distances_expanded(galaxies, rows, cols, 1)
    print(sum(distances))

    distances = find_distances_expanded(galaxies, rows, cols, 999999)
    print(sum(distances))
