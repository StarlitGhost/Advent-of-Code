from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2
from collections import defaultdict


def main():
    grid = Grid(aoc.read_lines())
    asteroids = list(grid.find_all('#'))

    most_seen = 0
    for asteroid in asteroids:
        angles = defaultdict(list)
        for other in asteroids:
            if other == asteroid:
                continue

            angle = (Vec2(other) - Vec2(asteroid)).north_angle()
            angles[angle].append(other)
            angles[angle].sort(key=lambda a: Vec2.manhattan_distance(asteroid, a))

        if len(angles) > most_seen:
            most_seen = len(angles)

    print('p1:', most_seen)


if __name__ == "__main__":
    main()
