from GhostyUtils import aoc
from GhostyUtils.vec2 import Vec2, Dir
from GhostyUtils.grid import Grid
from collections import Counter
import math
import pathlib
from PIL import Image, ImageDraw


aoc.argparser.add_argument("-d", "--dimensions", type=str, default="101,103",
                           help="width,height")
aoc.argparser.add_argument("-s", "--seconds", type=int, default=100)


class Rectangle:
    def __init__(self, top_left: Vec2, bottom_right: Vec2) -> 'Rectangle':
        self.tl = top_left
        self.br = bottom_right

    def contains(self, other: Vec2) -> bool:
        return ((self.tl.x <= other.x < self.br.x) and
                (self.tl.y <= other.y < self.br.y))


class Robot:
    def __init__(self, position: Vec2, velocity: Vec2) -> 'Robot':
        self.pos = position
        self.v = velocity

    def __str__(self) -> str:
        return f"p={self.pos.x},{self.pos.y} v={self.v.x},{self.v.y}"

    def step(self, grid: Grid):
        self.pos += self.v
        self.pos.x %= grid.width()
        self.pos.y %= grid.height()


def count_quadrants(robots: list[Robot], grid: Grid) -> list[int]:
    q_width = grid.width() // 2
    q_height = grid.height() // 2
    quadrants = [
        Rectangle(Vec2(0, 0), Vec2(q_width, q_height)),
        Rectangle(Vec2(q_width + 1, 0), Vec2(grid.width(), q_height)),
        Rectangle(Vec2(0, q_height + 1), Vec2(q_width, grid.height())),
        Rectangle(Vec2(q_width + 1, q_height + 1), Vec2(grid.width(), grid.height())),
    ]

    count = [0]*4
    for robot in robots:
        for q, quad in enumerate(quadrants):
            count[q] += 1 if quad.contains(robot.pos) else 0

    return count


def render_robots(robots: list[Robot], grid: Grid, seconds: int):
    image = Image.new(mode="1", size=(grid.width(), grid.height()), color=0)
    draw = ImageDraw.Draw(image)
    [draw.point(robot.pos.as_tuple(), fill=1) for robot in robots]
    pathlib.Path(f"{aoc.args.filename}_robots").mkdir(parents=True, exist_ok=True)
    image.save(f"{aoc.args.filename}_robots/{seconds}.png")

    # print(grid.render_with_overlays([Counter(robot.pos.as_tuple() for robot in robots)]))
    print(f"{seconds}/{math.prod(map(int, aoc.args.dimensions.split(',')))}")


def main():
    inputs = aoc.read_lines()

    robots = []
    for line in inputs:
        robots.append(Robot(*(Vec2.from_str(vec[2:], ',') for vec in line.split())))

    dimensions = Vec2.from_str(aoc.args.dimensions, ',')
    grid = Grid(['.' * dimensions.x] * dimensions.y)

    if aoc.args.progress or aoc.args.verbose:
        print("Initial state:")
        render_robots(robots, grid, seconds=0)
        print()

    for s in range(aoc.args.seconds):
        for robot in robots:
            robot.step(grid)

        if aoc.args.progress or aoc.args.verbose:
            print(f"After {s+1} second{'s' if s > 1 else ''}:")
            render_robots(robots, grid, seconds=s+1)
            print()

    print(f"p1: {math.prod(count_quadrants(robots, grid))}")

    most_horz_robots = 0
    best_second = 0
    for s in range(aoc.args.seconds, dimensions.x * dimensions.y):
        for robot in robots:
            robot.step(grid)

        robots.sort(key=lambda robot: robot.pos.as_tuple()[::-1])
        horz_robots = 1
        for r1, r2 in zip(robots, robots[1:]):
            if r1.pos + Dir.RIGHT == r2.pos:
                horz_robots += 1
            else:
                if horz_robots > most_horz_robots:
                    most_horz_robots = horz_robots
                    best_second = s+1
                horz_robots = 1

        if aoc.args.progress or aoc.args.verbose:
            render_robots(robots, grid, seconds=s+1)

    print(f"p2: {best_second}")


if __name__ == "__main__":
    main()
