from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Dir, Vec2


xmas_dirs = [
    Dir.EAST,
    Dir.SOUTH_EAST,
    Dir.SOUTH,
    Dir.SOUTH_WEST,
    Dir.WEST,
    Dir.NORTH_WEST,
    Dir.NORTH,
    Dir.NORTH_EAST,
]


def search_xmas(grid: Grid, pos: Vec2) -> int:
    xmas_count = 0
    for dir_ in xmas_dirs:
        word = [grid[pos + dir_.as_vec2() * i]
                for i in range(4) if grid.in_bounds(pos + dir_.as_vec2() * i)]
        if word == list('XMAS'):
            xmas_count += 1
            # print(pos, dir_, word)
    return xmas_count


def search_masx(grid: Grid, pos: Vec2) -> int:
    one = sorted([grid[pos + Dir.NORTH_EAST], grid[pos + Dir.SOUTH_WEST]])
    two = sorted([grid[pos + Dir.NORTH_WEST], grid[pos + Dir.SOUTH_EAST]])
    if one == two == list('MS'):
        return 1
    return 0


def main():
    grid = Grid(aoc.read_lines())

    xmas_count = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'X':
                xmas_count += search_xmas(grid, Vec2(x, y))
            else:
                continue
    print("p1:", xmas_count)

    masx_count = 0
    for y, row in enumerate(grid):
        # skip the top and bottom rows
        if y in [0, grid.height() - 1]:
            continue
        for x, cell in enumerate(row):
            # skip the left and right columns
            if x in [0, grid.width() - 1]:
                continue
            if cell == 'A':
                masx_count += search_masx(grid, Vec2(x, y))
            else:
                continue
    print("p2:", masx_count)


if __name__ == "__main__":
    main()
