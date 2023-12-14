from enum import Enum
from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2


class Dir(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


dir_offset = {Dir.WEST: Vec2(-1, 0),
              Dir.EAST: Vec2(1, 0),
              Dir.NORTH: Vec2(0, -1),
              Dir.SOUTH: Vec2(0, 1)}


class RollingRock:
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return "O"

    def roll(self, direction: Dir, grid: Grid):
        moveDir = dir_offset[direction]
        offset = self.pos
        while True:
            if not grid.vec2_inside(offset + moveDir):
                break
            ahead = grid[offset + moveDir]
            if ahead == '.':
                offset = offset + moveDir
            else:
                break
        grid[self.pos] = '.'
        self.pos = offset
        grid[self.pos] = self


class StaticRock:
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return "#"


def tilt(grid: Grid, direction: Dir):
    match direction:
        case Dir.NORTH:
            gridScan = grid.by_rows()
        case Dir.SOUTH:
            gridScan = reversed(list(grid.by_rows))
        case Dir.WEST:
            gridScan = grid.by_cols()
        case Dir.EAST:
            gridScan = reversed(list(grid.by_cols()))
    for row in gridScan:
        rocks = (rock for rock in row if type(rock) is RollingRock)
        for rock in rocks:
            rock.roll(direction, grid)


if __name__ == "__main__":
    grid = Grid(aoc.read_lines())
    rocks = []

    for pos in grid.find_all('O'):
        grid[pos] = RollingRock(pos)
        rocks.append(grid[pos])
    for pos in grid.find_all('#'):
        grid[pos] = StaticRock(pos)

    tilt(grid, Dir.NORTH)
    # print(grid)
    print(sum(grid.height() - rock.pos.y for rock in rocks))
