import sys
import functools

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    total_paper = 0
    total_ribbon = 0

    for i in inputs:
        sides = [int(s) for s in i.split('x')]
        areas = [2*sides[0]*sides[1], 2*sides[1]*sides[2], 2*sides[2]*sides[0]]
        paper = sum(areas) + min(areas)//2
        # print(f'{i} -> {areas} -> {sum(areas)} + {min(areas)//2} = {paper}')
        total_paper += paper

        short_sides = sorted(sides)[:2]
        wrap = short_sides[0]*2 + short_sides[1]*2
        bow = functools.reduce(lambda x, y: x*y, sides)
        ribbon = wrap + bow
        total_ribbon += ribbon

    print(total_paper)
    print(total_ribbon)
