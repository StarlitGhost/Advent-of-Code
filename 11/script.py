import sys
import itertools

def mh_distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)

def mh_distance_expanded(start, end, rows, cols, expansion):
    x1, y1 = start
    x2, y2 = end
    xdist = abs(x1 - x2)
    ydist = abs(y1 - y2)
    for col in cols:
        if (x1<x2 and x1 < col < x2) or (x2<x1 and x2 < col < x1):
            xdist += expansion
    for row in rows:
        if (y1<y2 and y1 < row < y2) or (y2<y1 and y2 < row < y1):
            ydist += expansion
    return xdist+ydist

def print_grid(grid):
    print()
    print('\n'.join(''.join(row) for row in grid))

def expansion_rows_cols(grid):
    expand_rows = [y for y, row in enumerate(grid) if all(x == '.' for x in row)]
    expand_columns = [x for x, col in enumerate(zip(*grid)) if all(y == '.' for y in col)]
    return expand_rows, expand_columns

def expand_space(grid, rows, cols, amount=1):
    for row in reversed(rows):
        for n in range(amount):
            grid.insert(row, grid[row][:])

    for col in reversed(cols):
        for row in grid:
            for n in range(amount):
                row.insert(col, '.')

def find_galaxies(grid):
    galaxies = []
    for y, row in enumerate(grid):
        for x, galaxy in enumerate(row):
            if galaxy == '#':
                galaxies.append((x,y))
    return galaxies

def find_distances(galaxies):
    distances = [mh_distance(pair[0], pair[1]) for pair in itertools.combinations(galaxies, 2)]
    return distances

def find_distances_expanded(galaxies, rows, cols, expansion):
    distances = [mh_distance_expanded(pair[0], pair[1], rows, cols, expansion)
                 for pair in itertools.combinations(galaxies, 2)]
    return distances

if __name__ == '__main__':
    inputs = open(sys.argv[1]).read().strip().split('\n')
    space = [[i for i in row] for row in inputs]

    rows, cols = expansion_rows_cols(space)
    galaxies = find_galaxies(space)
    distances = find_distances_expanded(galaxies, rows, cols, 1)
    print(sum(distances))

    space = [[i for i in row] for row in inputs]
    galaxies = find_galaxies(space)
    distances = find_distances_expanded(galaxies, rows, cols, 999999)
    print(sum(distances))
