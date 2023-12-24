from GhostyUtils import aoc
from GhostyUtils.vec3 import Vec3
import math
import itertools


MIN = 200000000000000
MAX = 400000000000000


def ray_intersection(ray_a, ray_b):
    a_pos, a_vel = ray_a
    b_pos, b_vel = ray_b
    dx = b_pos.x - a_pos.x
    dy = b_pos.y - a_pos.y
    det = b_vel.x * a_vel.y - b_vel.y * a_vel.x
    if det == 0:
        return False
    u = (dy * b_vel.x - dx * b_vel.y) / det
    v = (dy * a_vel.x - dx * a_vel.y) / det
    p = a_pos + a_vel * u
    return p, (u, v)


if __name__ == "__main__":
    hail = []
    for hail_txt in aoc.read_lines():
        pos, v = hail_txt.split(' @ ')
        pos = Vec3(tuple(map(int, pos.split(', '))))
        v = Vec3(tuple(map(int, v.split(', '))))
        hail.append((pos, v))

    collisions_in_area = 0
    for t1, t2 in itertools.combinations(hail, 2):
        print(f'Hailstone A: {t1[0]} @ {t1[1]}')
        print(f'Hailstone B: {t2[0]} @ {t2[1]}')
        result = ray_intersection(t1, t2)
        if result:
            p, (u, v) = result
            if u < 0 and v < 0:
                print("Hailstones' paths crossed in the past for both hailstones")
            elif u < 0:
                print("Hailstones' paths crossed in the past for hailstone A")
            elif v < 0:
                print("Hailstones' paths crossed in the past for hailstone B")
            elif MIN <= p.x <= MAX and MIN <= p.y <= MAX:
                collisions_in_area += 1
                print(f"Hailstones' paths will cross inside the test area (at {p})")
            else:
                print(f"Hailstones' paths will cross outside the test area (at {p})")
        else:
            print("Hailstones' paths are parallel; they never intersect")
        print()

    print('p1:', collisions_in_area)
