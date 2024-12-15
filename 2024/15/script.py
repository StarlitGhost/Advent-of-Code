from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir


class Robot:
    def __init__(self, pos: Vec2) -> 'Robot':
        self.pos = Vec2(pos)

    def move(self, dir: Dir, grid: Grid) -> bool:
        if grid[self.pos + dir].move(dir, grid):
            grid[self.pos] = Air(self.pos)
            self.pos += dir
            grid[self.pos] = self
            return True
        return False

    def __str__(self) -> str:
        return '@'


class Box:
    def __init__(self, pos: Vec2) -> 'Box':
        self.pos = Vec2(pos)

    def move(self, dir: Dir, grid: Grid) -> bool:
        if grid[self.pos + dir].move(dir, grid):
            grid[self.pos] = Air(self.pos)
            self.pos += dir
            grid[self.pos] = self
            return True
        return False

    def __str__(self) -> str:
        return 'O'


class Wall:
    def __init__(self, pos: Vec2) -> 'Wall':
        self.pos = Vec2(pos)

    def move(self, dir: Dir, grid: Grid) -> bool:
        return False

    def __str__(self) -> str:
        return '#'


class Air:
    def __init__(self, pos: Vec2) -> 'Air':
        pass

    def move(self, dir: Dir, grid: Grid) -> bool:
        return True

    def __str__(self) -> str:
        return '.'


def convert(cell: str, pos: Vec2) -> Robot | Box | Wall | Air:
    return {'@': Robot, '#': Wall, 'O': Box, '.': Air}[cell](pos)


def main():
    warehouse, instructions = aoc.read_sections()
    warehouse = Grid(warehouse.splitlines())
    robot = None
    boxes = []
    for cell, pos in warehouse.by_cell():
        warehouse[pos] = convert(cell, pos)
        if type(warehouse[pos]) is Box:
            boxes.append(warehouse[pos])
        elif type(warehouse[pos]) is Robot:
            robot = warehouse[pos]

    if aoc.args.verbose or aoc.args.progress:
        print(warehouse)

    for instr in instructions:
        if instr == '\n':
            continue
        robot.move(Dir.map_nswe('^v<>')[instr], warehouse)

        if aoc.args.verbose or aoc.args.progress:
            print(warehouse)

    print(f"p1: {sum(box.pos.y * 100 + box.pos.x for box in boxes)}")


if __name__ == "__main__":
    main()
