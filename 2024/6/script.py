from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir


def move(pos: tuple, dir_: Dir, grid: Grid) -> tuple[tuple, Dir]:
    next_pos = pos + Vec2(dir_)

    # out of bounds or open, return next position
    if not grid.in_bounds(next_pos) or not grid[next_pos] == '#':
        return next_pos, dir_

    # obstacle, rotate right 90 degrees
    else:
        return pos, dir_.turn_right()


def main():
    grid = Grid(aoc.read_lines())
    print(grid)

    pos = grid.find('^')
    dir_ = Dir.UP

    visited = set()
    visited.add(pos)
    while grid.in_bounds(pos):
        pos, dir_ = move(pos, dir_, grid)
        visited.add(pos.as_tuple())

    print("p1:", len(visited) - 1)


if __name__ == "__main__":
    main()
