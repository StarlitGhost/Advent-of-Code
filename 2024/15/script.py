from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir
from typing import Union


class Robot:
    def __init__(self, pos: Vec2) -> 'Robot':
        self.pos = Vec2(pos)

    def process(self, instructions: str, grid: Grid):
        for instr in instructions:
            if instr == '\n':
                continue
            self.move(Dir.map_nswe('^v<>')[instr], grid)

            if aoc.args.verbose:
                print(instr)
                print(grid)

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
        self.width = 1
        self.last_draw = -1

    def touching(self, dir: Dir, grid: Grid) -> set[Union['Box', 'Wall', 'Air']]:
        if dir in {Dir.NORTH, Dir.SOUTH}:
            cells = filter(lambda c: type(c) is not Air,
                           (grid[self.pos + Vec2(Dir.EAST) * i + dir]
                            for i in range(self.width)))
        else:
            cells = filter(lambda c: type(c) is not Air,
                           [grid[self.pos + (dir if dir == Dir.WEST else Vec2(dir) * self.width)]])
        cells = set(cells)

        return cells

    def can_move(self, dir: Dir, grid: Grid) -> bool:
        return all(cell.can_move(dir, grid) for cell in self.touching(dir, grid))

    def move(self, dir: Dir, grid: Grid) -> bool:
        if not self.can_move(dir, grid):
            return False

        for cell in self.touching(dir, grid):
            grid[cell.pos].move(dir, grid)

        self.pos += dir
        if dir == Dir.WEST:
            grid[self.pos + Vec2(Dir.EAST) * self.width] = Air(None)
            for i in range(self.width):
                grid[self.pos + Vec2(Dir.EAST) * i] = self
        elif dir == Dir.EAST:
            grid[self.pos + Vec2(Dir.WEST)] = Air(None)
            for i in range(self.width):
                grid[self.pos + Vec2(Dir.EAST) * i] = self
        else:
            for i in range(self.width):
                grid[self.pos + Vec2(Dir.EAST) * i - dir] = Air(None)
                grid[self.pos + Vec2(Dir.EAST) * i] = self
        return True

    def gps(self) -> int:
        return 100 * self.pos.y + self.pos.x

    def __str__(self) -> str:
        if self.width == 1:
            return 'O'
        elif self.width == 2:
            self.last_draw += 1
            if self.last_draw > 1:
                self.last_draw = 0
            return '[]'[self.last_draw]

    def __repr__(self) -> str:
        return f"Box at {self.pos}"


class Wall:
    def __init__(self, pos: Vec2) -> 'Wall':
        self.pos = Vec2(pos)

    def move(self, dir: Dir, grid: Grid) -> bool:
        return False

    def can_move(self, dir: Dir, grid: Grid) -> bool:
        return False

    def __str__(self) -> str:
        return '#'

    def __repr__(self) -> str:
        return f"Wall at {self.pos}"


class Air:
    def __init__(self, pos: Vec2) -> 'Air':
        pass

    def move(self, dir: Dir, grid: Grid) -> bool:
        return True

    def can_move(self, dir: Dir, grid: Grid) -> bool:
        return True

    def __str__(self) -> str:
        return '.'


def build_warehouse(floorplan: str, wide: bool = False) -> tuple[Grid, Robot, list[Box]]:
    floorplan = floorplan.splitlines()
    if wide:
        new_floorplan = []
        for row in floorplan:
            new_row = []
            for c in row:
                new_row.append({'#': '##', '@': '@.', 'O': '[]', '.': '..'}[c])
            new_floorplan.append(''.join(new_row))
        floorplan = new_floorplan

    warehouse = Grid(floorplan)
    robot = None
    boxes = []
    for cell, pos in warehouse.by_cell():
        if cell == ']':
            warehouse[pos] = warehouse[Vec2(pos) + Dir.WEST]
            warehouse[pos].width = 2
            continue
        warehouse[pos] = convert(cell, pos)
        if type(warehouse[pos]) is Box:
            boxes.append(warehouse[pos])
        elif type(warehouse[pos]) is Robot:
            robot = warehouse[pos]
    return warehouse, robot, boxes


def convert(cell: str, pos: Vec2) -> Robot | Box | Wall | Air:
    return {
        '@': Robot,
        'O': Box,
        '[': Box,
        '#': Wall,
        '.': Air
    }[cell](pos)


def main():
    floorplan, instructions = aoc.read_sections()

    warehouse, robot, boxes = build_warehouse(floorplan)
    if aoc.args.verbose or aoc.args.progress:
        print(warehouse)
    robot.process(instructions, warehouse)
    if aoc.args.progress:
        print(warehouse)
    print(f"p1: {sum(box.gps() for box in boxes)}")

    warehouse, robot, boxes = build_warehouse(floorplan, wide=True)
    if aoc.args.verbose or aoc.args.progress:
        print(warehouse)
    robot.process(instructions, warehouse)
    if aoc.args.progress:
        print(warehouse)
    print(f"p2: {sum(box.gps() for box in boxes)}")


if __name__ == "__main__":
    main()
