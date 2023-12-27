from GhostyUtils import aoc
from GhostyUtils.vec3 import Vec3
import re
import itertools


def energy(moon: dict) -> int:
    pot = sum(map(abs, moon['pos']))
    kin = sum(map(abs, moon['v']))
    total = pot * kin
    return total


def apply_gravity(moons: list[dict]):
    for pair in itertools.combinations(moons, 2):
        m1, m2 = pair
        for i, component in enumerate(zip(m1['pos'], m2['pos'])):
            a, b = component
            if a < b:
                m1['v'][i] += 1
                m2['v'][i] -= 1
            elif a > b:
                m1['v'][i] -= 1
                m2['v'][i] += 1
            else:
                pass


def apply_velocity(moons: list[dict]):
    for moon in moons:
        moon['pos'] += moon['v']


def vec_str(v: Vec3) -> str:
    return f"<x={v.x:3,d}, y={v.y:3,d}, z={v.z:3,d}>"


def print_moons(moons: list[dict]):
    for moon in moons:
        p = moon['pos']
        v = moon['v']
        print(f"pos={vec_str(p)}, vel={vec_str(v)} | {moon['name']}")


def main():
    names = ['Io', 'Europa', 'Ganymede', 'Callisto']
    moons = [
        {'pos': Vec3(*map(int, re.sub(r'[<>=xyz ]', '', line).split(','))),
         'v': Vec3(0, 0, 0)}
        for line in aoc.read_lines()]
    [moons[i].__setitem__('name', name) for i, name in enumerate(names)]

    print("After 0 steps:")
    print_moons(moons)
    print()

    steps = 1000
    for step in range(1, steps+1):
        apply_gravity(moons)
        apply_velocity(moons)

        print(f"After {step} steps:")
        print_moons(moons)
        print()

    print('p1:', sum(map(energy, moons)))


if __name__ == "__main__":
    main()
