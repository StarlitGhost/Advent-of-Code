from GhostyUtils import aoc
import itertools
from string import ascii_uppercase
from collections import defaultdict


def add(t1: tuple, t2: tuple):
    """adds two tuples of the same length element-wise"""
    return tuple(map(sum, zip(t1, t2)))


def iter_labels():
    """yields incrementing labels of the form A, B, ..., Z, AA, AB, ..."""
    for size in itertools.count(1):
        for s in itertools.product(ascii_uppercase, repeat=size):
            yield "".join(s)


def fall(grid: dict, brick: tuple[tuple, tuple], label: str) -> set[str]:
    # find brick orientation
    x_footprint = abs(brick[0][0] - brick[1][0])
    y_footprint = abs(brick[0][1] - brick[1][1])
    if x_footprint >= 1:
        scan_dir = (1, 0, 0)
    elif y_footprint >= 1:
        scan_dir = (0, 1, 0)
    else:
        scan_dir = (0, 0, 1)

    # scan downwards from each grid cell within the brick's horizontal footprint
    min_z = min(brick[0][2], brick[1][2])
    start = min(brick[0], brick[1])
    end = max(brick[0], brick[1])
    scan = start
    offset = (0, 0, -min_z+1)
    while scan != add(end, scan_dir):
        for z in range(1, min_z):
            scan_z = add(scan, (0, 0, -z))
            # we found another brick!
            if scan_z in grid:
                # update our resting offset if higher than we already found
                if (0, 0, -z+1) > offset:
                    offset = (0, 0, -z+1)
                break
        # if the brick is vertical, we only need to scan down once
        if scan_dir == (0, 0, 1):
            break
        # move onto the next scan position
        scan = add(scan, scan_dir)

    # calculate the brick's resting positions
    rest_start = add(start, offset)
    rest_end = add(end, offset)
    rest = rest_start
    sitting_on = set()
    # scan along the brick's resting positions and write to the grid
    while rest != add(rest_end, scan_dir):
        below = add(rest, (0, 0, -1))
        # if there's a brick directly below this position, add it to sitting_on
        if below in grid and grid[below] != label:
            # print(label, 'sits on', grid[below])
            sitting_on.add(grid[below])
        grid[rest] = label
        rest = add(rest, scan_dir)

    return sitting_on


if __name__ == "__main__":
    # sparse grid, (x,y,z): 'brick label'
    grid = {}

    # read & parse in our bricks
    bricks_txt = aoc.read_lines()
    bricks = []
    labels = iter_labels()
    for i, b in enumerate(bricks_txt):
        start, end = b.split('~')
        start = tuple(map(int, start.split(',')))
        end = tuple(map(int, end.split(',')))
        bricks.append((start, end))

    # sort bricks by z-height
    bricks.sort(key=lambda b: min(b[0][2], b[1][2]))

    # drop our bricks into the grid, from lowest to highest
    sitting_on = {}
    supporting = defaultdict(set)
    for brick in bricks:
        label = next(labels)
        sitting_on[label] = fall(grid, brick, label)
        for b in sitting_on[label]:
            supporting[b].add(label)
#   print(sitting_on)

    # find bricks that are safe to remove
    # first add all the bricks to the safe set, then remove those found unsafe
    safe = set(sitting_on.keys())
    unsafe = set()
    for below in sitting_on.values():
        # the brick below is unsafe if it is our only support
        if len(below) == 1 and next(iter(below)) in safe:
            safe.remove(*below)
            unsafe.add(*below)
#   print(safe)

    print('p1:', len(safe))

#   print(unsafe)
#   print(supporting)

    def will_fall(falls, brick):
        for brick_above in supporting[brick]:
            if len(sitting_on[brick_above] - falls) <= 1:
                falls.add(brick_above)
                will_fall(falls, brick_above)

    total_falls = 0
    for brick in unsafe:
        falls = set()
        will_fall(falls, brick)
        total_falls += len(falls)
    print('p2:', total_falls)
