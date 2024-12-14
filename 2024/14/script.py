from GhostyUtils import aoc
from GhostyUtils.vec2 import Vec2
from GhostyUtils.grid import Grid
from collections import Counter
import math


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


def render_robots(robots: list[Robot], grid: Grid) -> str:
    return grid.render_with_overlays([Counter(robot.pos.as_tuple() for robot in robots)])


def main():
    inputs = aoc.read_lines()

    robots = []
    for line in inputs:
        robots.append(Robot(*(Vec2.from_str(vec[2:], ',') for vec in line.split())))

    dimensions = Vec2.from_str(aoc.args.dimensions, ',')
    grid = Grid(['.' * dimensions.x] * dimensions.y)

    print("Initial state:")
    print(render_robots(robots, grid))
    print()
    for s in range(aoc.args.seconds):
        for robot in robots:
            robot.step(grid)

        print(f"After {s+1} second{'s' if s > 1 else ''}:")
        print(render_robots(robots, grid))
        print()

    print(f"p1: {math.prod(count_quadrants(robots, grid))}")


if __name__ == "__main__":
    main()
