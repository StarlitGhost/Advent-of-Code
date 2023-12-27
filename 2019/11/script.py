from GhostyUtils import aoc
from GhostyUtils.intcode.cpu import IntCode
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2, Dir


class Robot:
    def __init__(self, pos: Vec2, dir: Dir, grid: dict):
        self.pos = pos
        self.dir = dir
        self.next = 0
        self.grid = grid
        self.cpu = IntCode(aoc.read(), input=self.camera, output=self.control)

    def run(self):
        self.cpu.process()

    def camera(self):
        if tuple(self.pos) in self.grid:
            return self.grid[tuple(self.pos)]
        return 0

    def control(self, output: int):
        if self.next == 0:
            self.paint(output)
        elif self.next == 1:
            self.turn(output)
            self.move()
        self.next = (self.next + 1) % 2

    def paint(self, color: int):
        self.grid[tuple(self.pos)] = color

    def turn(self, lr: int):
        turns = [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT]
        cur_idx = turns.index(self.dir)
        turn_idx = (cur_idx+(1 if lr == 1 else -1)) % len(turns)
        self.dir = turns[turn_idx]

    def move(self):
        self.pos += self.dir


def make_grid(grid: dict) -> Grid:
    tl = Vec2(min(grid.keys(), key=lambda pos: pos[0])[0],
              min(grid.keys(), key=lambda pos: pos[1])[1])
    br = Vec2(max(grid.keys(), key=lambda pos: pos[0])[0],
              max(grid.keys(), key=lambda pos: pos[1])[1])
    width = br.x - tl.x + 1
    height = br.y - tl.y + 1
    new_grid = Grid(' ' * width for _ in range(height))
    for coord, paint in grid.items():
        new_grid[tuple(coord - tl)] = '#' if paint else ' '
    return new_grid


def main():
    grid = {}
    robot = Robot(Vec2(0, 0), Dir.UP, grid)
    robot.run()
    print('p1:', len(grid))
#   print(make_grid(grid))

    grid = {(0, 0): 1}
    robot = Robot(Vec2(0, 0), Dir.UP, grid)
    robot.run()
    print(make_grid(grid))


if __name__ == "__main__":
    main()
