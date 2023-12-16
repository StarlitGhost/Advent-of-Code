from functools import cache
from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir


@cache
def walk(start: tuple, target: tuple, direction: tuple) -> tuple[tuple]:
    def _walk(start, target, direction):
        pos = Vec2(*start)
        target = Vec2(*target)
        dir_ = Vec2(*direction)
        while pos != target:
            yield pos.as_tuple()
            pos += dir_
        yield pos.as_tuple()
    return tuple(pos for pos in _walk(start, target, direction))


class Obstacles:
    def __init__(self, vert_splitters, horz_splitters, mirrors):
        self.vertical = tuple(v.as_tuple() for v in
                              sorted(horz_splitters + mirrors, key=lambda v: v.y))
        self.horizontal = tuple(v.as_tuple() for v in
                                sorted(vert_splitters + mirrors, key=lambda v: v.x))
        self.cache = {}

    def get(self, start: tuple, direction: tuple) -> Vec2:
        if (start, direction) in self.cache:
            return self.cache[(start, direction)]

        s = start
        match Dir(direction):
            case Dir.NORTH:
                ob = filter(lambda v: v[1] <= s[1] and v[0] == s[0], reversed(self.vertical))
            case Dir.SOUTH:
                ob = filter(lambda v: v[1] >= s[1] and v[0] == s[0], self.vertical)
            case Dir.EAST:
                ob = filter(lambda v: v[0] >= s[0] and v[1] == s[1], self.horizontal)
            case Dir.WEST:
                ob = filter(lambda v: v[0] <= s[0] and v[1] == s[1], reversed(self.horizontal))
        ob = next(ob, None)
        if ob:
            ob = Vec2(*ob)

        self.cache[(start, direction)] = ob

        return ob


class Beam:
    def __init__(self, pos: Vec2, direction: Dir):
        self.pos = pos
        self.dir_ = direction

    def __repr__(self):
        return f'{{origin: {self.pos.as_tuple()}, dir: {self.dir_.name}}}'

    def as_tuple(self):
        return (self.pos.as_tuple(), self.dir_.value)

    def trace(self, grid: Grid, obstacles: Obstacles):
        ob = obstacles.get(self.pos.as_tuple(), self.dir_.value)
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

        ob_pos = ob
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

    def walk(self, target):
        return walk(self.pos.as_tuple(), target.as_tuple(), self.dir_.value)



def beam_coverage(starting_beam: Beam, grid: Grid, obstacles: Obstacles) -> int:
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
    return len(coverage)


if __name__ == "__main__":
    grid = Grid(aoc.read_lines())
    vert_splitters = tuple(grid.find_all('|'))
    horz_splitters = tuple(grid.find_all('-'))
    mirrors = tuple(grid.find_all('\\')) + tuple(grid.find_all('/'))
    obstacles = Obstacles(vert_splitters, horz_splitters, mirrors)

    beam = Beam(Vec2(0, 0), Dir.EAST)
    print(beam_coverage(beam, grid, obstacles))

    best_coverage = 0
    best_beam = None

    def gen_beams():
        for beam in (Beam(Vec2(0, y), Dir.EAST) for y in range(grid.height())):
            yield beam
        for beam in (Beam(Vec2(grid.width()-1, y), Dir.WEST) for y in range(grid.height())):
            yield beam
        for beam in (Beam(Vec2(x, grid.height()-1), Dir.NORTH) for x in range(grid.width())):
            yield beam
        for beam in (Beam(Vec2(x, 0), Dir.SOUTH) for x in range(grid.width())):
            yield beam

    for beam in gen_beams():
        coverage = beam_coverage(beam, grid, obstacles)
        if coverage > best_coverage:
            best_coverage = coverage
            best_beam = beam
    print(best_coverage, best_beam)
