from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Dir, Vec2


def search_xmas(grid: Grid, pos: Vec2) -> int:
    xmas_count = 0
    for dir_ in [Dir.E, Dir.SE, Dir.S, Dir.SW, Dir.W, Dir.NW, Dir.N, Dir.NE]:
        word = [grid[pos + Vec2(dir_) * i]
                for i in range(4) if grid.in_bounds(pos + Vec2(dir_) * i)]
        if word == list('XMAS'):
            xmas_count += 1
            # print(pos, dir_, word)
    return xmas_count


def search_masx(grid: Grid, pos: Vec2) -> int:
    # skip As at the edge of the grid
    if pos.x in [0, grid.width() - 1] or pos.y in [0, grid.height() - 1]:
        return 0
    one = sorted([grid[pos + Dir.NE], grid[pos + Dir.SW]])
    two = sorted([grid[pos + Dir.NW], grid[pos + Dir.SE]])
    if one == two == list('MS'):
        return 1
    return 0


def main():
    grid = Grid(aoc.read_lines())

    print("p1:", sum(search_xmas(grid, Vec2(pos)) for pos in grid.find_all('X')))
    print("p2:", sum(search_masx(grid, Vec2(pos)) for pos in grid.find_all('A')))


if __name__ == "__main__":
    main()
