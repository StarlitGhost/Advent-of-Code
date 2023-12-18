from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir
from typing import Iterable


charmap = {
    Dir.UP.value: '^',
    Dir.DOWN.value: 'v',
    Dir.LEFT.value: '<',
    Dir.RIGHT.value: '>',
    None: '.',
}


class Cell:
    def __init__(self, pos, direction=None, colour=None):
        self.pos = pos
        self.direction = direction
        self.colour = colour

    def __str__(self):
        return charmap[self.direction]


def walk(start: tuple, target: tuple) -> tuple[tuple]:
    def _walk(start, target):
        pos = Vec2(*start)
        target = Vec2(*target)
        dir_ = (target - pos).unit()
        while pos != target:
            yield pos.as_tuple()
            pos += dir_
        yield pos.as_tuple()
    return tuple(pos for pos in _walk(start, target))


def count_inside(grid: Grid) -> int:
    total = 0
    for row in grid:
        inside = False
        for cell in row:
            if not inside and cell.direction == Dir.UP.value:
                inside = True
            if inside or cell.direction is not None:
                total += 1
            if inside and cell.direction is None:
                grid[cell.pos] = '#'
            if inside and cell.direction == Dir.DOWN.value:
                inside = False
    return total


def shoelace(points: Iterable[tuple], count_perimeter=True) -> int:
    area = 0
    perimeter = 0
    for p, pn in zip(points, points[1:]):
        area += p[0]*pn[1] - p[1]*pn[0]
        perimeter += abs(Vec2(pn) - Vec2(p))
    area /= 2
    area += (perimeter/2) + 1 if count_perimeter else -(perimeter/2) + 1
    return area


if __name__ == "__main__":
    plan_text = aoc.read_lines()

    # p1
    dirs = {'U': Dir.UP, 'D': Dir.DOWN, 'L': Dir.LEFT, 'R': Dir.RIGHT}
    plan = []
    for d, distance, col in map(str.split, plan_text):
        plan.append((dirs[d].value, int(distance), col))

    route = set()
    pos = (0, 0)
    points = [pos]
    perimeter = 0
    for step in plan:
        d, dist, col = step
        target = pos + Vec2(d) * dist
        route.update((pos, d, col) for pos in walk(pos, target))
        perimeter += abs(target - pos)
        pos = target.as_tuple()
        points.append(pos)
    tl = (min(route, key=lambda r: r[0][0])[0][0], min(route, key=lambda r: r[0][1])[0][1])
    br = (max(route, key=lambda r: r[0][0])[0][0], max(route, key=lambda r: r[0][1])[0][1])
    width = br[0]-tl[0]+1
    height = br[1]-tl[1]+1
    grid = Grid([[Cell((x, y)) for x in range(width)] for y in range(height)])
    for r in route:
        pos = Vec2(r[0]) - tl
        if grid[pos].direction in [(1, 0), (-1, 0), None]:
            grid[pos] = Cell(pos, r[1], r[2])
    total = count_inside(grid)
    print(grid)
    print('p1', 'scan:', total, 'shoelace:', int(shoelace(points)))

    # p2
    dirs = {0: Dir.RIGHT.value, 1: Dir.DOWN.value, 2: Dir.LEFT.value, 3: Dir.UP.value}
    plan = []
    for _, _, col in map(str.split, plan_text):
        d = dirs[int(col[-2:-1])]
        distance = int(col[-7:-2], 16)
        plan.append((d, distance))

    pos = (0, 0)
    points = [pos]
    perimeter = 0
    for step in plan:
        d, dist = step
        target = pos + Vec2(d) * dist
        perimeter += abs(target - pos)
        pos = target.as_tuple()
        points.append(pos)
    print('p2', 'shoelace:', int(shoelace(points)))
