from typing import Iterable
from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir


class Obstacles:
    def __init__(self, vert_splitters, horz_splitters, mirrors):
        self.vertical = sorted(horz_splitters + mirrors, key=lambda v: v.y)
        self.horizontal = sorted(vert_splitters + mirrors, key=lambda v: v.x)


class Beam:
    def __init__(self, pos: Vec2, direction: Dir):
        self.pos = pos
        self.dir_ = direction

    def __repr__(self):
        return f'{{origin: {self.pos.as_tuple()}, dir: {self.dir_.name}}}'

    def as_tuple(self):
        return (self.pos.as_tuple(), self.dir_.value)

    def trace(self, grid: Grid, obstacles: Obstacles):# -> list[tuple], list['Beam']:
        match self.dir_:
            case Dir.NORTH:
                ob = filter(lambda v: v.y <= self.pos.y and v.x == self.pos.x,
                            reversed(obstacles.vertical))
            case Dir.SOUTH:
                ob = filter(lambda v: v.y >= self.pos.y and v.x == self.pos.x,
                            obstacles.vertical)
            case Dir.EAST:
                ob = filter(lambda v: v.x >= self.pos.x and v.y == self.pos.y,
                            obstacles.horizontal)
            case Dir.WEST:
                ob = filter(lambda v: v.x <= self.pos.x and v.y == self.pos.y,
                            reversed(obstacles.horizontal))
        ob = list(ob)
        if not ob:
            match self.dir_:
                case Dir.NORTH:
                    target = Vec2(self.pos.x, 0)
                case Dir.SOUTH:
                    target = Vec2(self.pos.x, grid.height()-1)
                case Dir.EAST:
                    target = Vec2(grid.width()-1, self.pos.y)
                case Dir.WEST:
                    target = Vec2(0, self.pos.y)
            # print('#', target.as_tuple())
            return self.walk(target), []

        ob_pos = ob[0]
        ob = grid[ob_pos]
        # print(ob, ob_pos.as_tuple())
        if self.dir_ in [Dir.NORTH, Dir.SOUTH]:
            if ob == '-':
                return self.walk(ob_pos), [Beam(ob_pos + Dir.WEST.as_vec2(), Dir.WEST),
                                           Beam(ob_pos + Dir.EAST.as_vec2(), Dir.EAST)]
            if ob == '\\':
                d = {Dir.NORTH: Dir.WEST, Dir.SOUTH: Dir.EAST}[self.dir_]
            elif ob == '/':
                d = {Dir.NORTH: Dir.EAST, Dir.SOUTH: Dir.WEST}[self.dir_]
        else:
            if ob == '|':
                return self.walk(ob_pos), [Beam(ob_pos + Dir.NORTH.as_vec2(), Dir.NORTH),
                                           Beam(ob_pos + Dir.SOUTH.as_vec2(), Dir.SOUTH)]
            if ob == '\\':
                d = {Dir.WEST: Dir.NORTH, Dir.EAST: Dir.SOUTH}[self.dir_]
            elif ob == '/':
                d = {Dir.EAST: Dir.NORTH, Dir.WEST: Dir.SOUTH}[self.dir_]
        return self.walk(ob_pos), [Beam(ob_pos + d.as_vec2(), d)]

    def walk(self, target) -> list[tuple]:
        def _walk(target):
            while self.pos != target:
                yield self.pos.as_tuple()
                self.pos += self.dir_.as_vec2()
            yield self.pos.as_tuple()
        return [pos for pos in _walk(target)]


if __name__ == "__main__":
    grid = Grid(aoc.read_lines())
    vert_splitters = tuple(grid.find_all('|'))
    horz_splitters = tuple(grid.find_all('-'))
    mirrors = tuple(grid.find_all('\\')) + tuple(grid.find_all('/'))
    obstacles = Obstacles(vert_splitters, horz_splitters, mirrors)

    starting_beam = Beam(Vec2(0, 0), Dir.EAST)
    beams = [starting_beam]

    coverage = set()
    seen_beams = set()
    seen_beams.add(starting_beam.as_tuple())

    # print(grid)

    while beams:
        new_beams = []
        for beam in beams:
            covers, beams_new = beam.trace(grid, obstacles)
            # print(covers, beams_new)
            for b in beams_new:
                if b.as_tuple() in seen_beams:
                    # print(f'seen {b}, skipped')
                    continue
                else:
                    seen_beams.add(b.as_tuple())
                if not grid.vec2_inside(b.pos):
                    continue
                new_beams.append(b)
            coverage.update(covers)
        beams = new_beams
    print(len(coverage))
