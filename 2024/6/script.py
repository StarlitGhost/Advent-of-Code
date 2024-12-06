from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir


def move(pos: Vec2, dir_: Dir, grid: Grid) -> tuple[Vec2, Dir]:
    if not grid.in_bounds(pos + Vec2(dir_)) or not grid[pos + Vec2(dir_)] == '#':
        return pos + Vec2(dir_), dir_
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
