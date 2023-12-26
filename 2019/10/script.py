from GhostyUtils import aoc
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2
from collections import defaultdict


def main():
    grid = Grid(aoc.read_lines())
    asteroids = list(grid.find_all('#'))

    most_seen = 0
    best_asteroid = None
    best_angles = {}
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
            best_asteroid = asteroid
            best_angles = angles

    print('p1:', most_seen, best_asteroid)

    angles = sorted(best_angles.keys())
    vaporised = 0
    last_vaporised = None
    empty = []
    while vaporised != 200:
        for angle in angles:
            if best_angles[angle]:
                last_vaporised = Vec2(best_angles[angle].pop(0))
                vaporised += 1
                if vaporised == 200:
                    break
                if not best_angles[angle]:
                    empty.append(angle)
        for angle in empty:
            del best_angles[angle]
    print('p2:', last_vaporised.x * 100 + last_vaporised.y, last_vaporised)


if __name__ == "__main__":
    main()
