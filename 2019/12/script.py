from GhostyUtils import aoc
from GhostyUtils.vec3 import Vec3
import re
import itertools
import math


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


def tupleize(moons: list[dict]) -> tuple[tuple, tuple, tuple]:
    x = tuple((moon['pos'].x, moon['v'].x) for moon in moons)
    y = tuple((moon['pos'].y, moon['v'].y) for moon in moons)
    z = tuple((moon['pos'].z, moon['v'].z) for moon in moons)
    return x, y, z


def record_history(history, x, y, z):
    all_looped = True
    if x not in history['x']:
        history['x'].add(x)
        all_looped = False
    if y not in history['y']:
        history['y'].add(y)
        all_looped = False
    if z not in history['z']:
        history['z'].add(z)
        all_looped = False
    return all_looped


def main():
    names = ['Io', 'Europa', 'Ganymede', 'Callisto']
    moons = [
        {'pos': Vec3(*map(int, re.sub(r'[<>=xyz ]', '', line).split(','))),
         'v': Vec3(0, 0, 0)}
        for line in aoc.read_lines()]
    [moons[i].__setitem__('name', name) for i, name in enumerate(names)]

#   print("After 0 steps:")
#   print_moons(moons)
#   print()

    history = {'x': set(), 'y': set(), 'z': set()}
    x, y, z = tupleize(moons)
    record_history(history, x, y, z)
    step = 1
    steps = 1000
    done = False
    while not done or step < steps:
        step += 1
        apply_gravity(moons)
        apply_velocity(moons)

        x, y, z = tupleize(moons)
        done = record_history(history, x, y, z)

#       print(f"After {step} steps:")
#       print_moons(moons)
#       print()

        if step == 1000:
            print('p1:', sum(map(energy, moons)))

    print('p2:', math.lcm(*tuple(len(s) for s in history.values())))


if __name__ == "__main__":
    main()
