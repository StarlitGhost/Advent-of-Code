from GhostyUtils import aoc
from GhostyUtils.vec2 import Vec2, Dir, manhattan_distance
from collections import defaultdict
import sys


def create_wire(wire: list[str]) -> set:
    start = Vec2(0, 0)
    points = set()
    steps = 0
    visited = defaultdict(list)
    for v in wire:
        d = Vec2(Dir.map_udlr('UDLR')[v[0]])
        magnitude = int(v[1:])
        offset = d * magnitude
        end = start + offset
        while start != end:
            points.add(tuple(start))
            visited[tuple(start)].append(steps)
            start += d
            steps += 1
    points.remove((0, 0))
    del visited[(0, 0)]
    return points, visited


def closest_intersection(wires):
    points = wires[0][0].intersection(wires[1][0])
    visited = [v for _, v in wires]
    closest = sys.maxsize
    fewest_combined_steps = sys.maxsize
    for p in points:
        dist = manhattan_distance((0, 0), p)
        if dist < closest:
            closest = dist

        for f_visit in visited[0][p]:
            for s_visit in visited[1][p]:
                combined_steps = f_visit + s_visit
                if combined_steps < fewest_combined_steps:
                    fewest_combined_steps = combined_steps

    return closest, fewest_combined_steps


def test():
    tests = [[['R75,D30,R83,U83,L12,D49,R71,U7,L72',
               'U62,R66,U55,R34,D71,R55,D58,R83'],
              159, 610],
             [['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
               'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'],
              135, 410]]
    for str_wires, r_closest, r_fewest in tests:
        wires = [create_wire(w.split(',')) for w in str_wires]
        closest, fewest = closest_intersection(wires)
        assert closest == r_closest, f'closest {closest} != r_closest {r_closest}'
        assert fewest == r_fewest, f'fewest {fewest} != r_fewest {r_fewest}'


if __name__ == "__main__":
    test()

    wires = [create_wire(w.split(',')) for w in aoc.read_lines()]

    closest, fewest = closest_intersection(wires)

    print('p1:', closest)
    print('p2:', fewest)
