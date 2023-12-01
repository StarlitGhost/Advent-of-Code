import sys

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    grid = [[0 for x in range(1000)] for y in range(1000)]

    def coord(s):
        return tuple([int(i) for i in s.split(',')])

    def turn(state, tl, br):
        # print(state, tl, br, (br[0]+1-tl[0])*(br[1]+1-tl[1]))
        for y in range(tl[1], br[1] + 1):
            for x in range(tl[0], br[0] + 1):
                grid[y][x] = state

    def toggle(tl, br):
        # print('~', tl, br, (br[0]+1-tl[0])*(br[1]+1-tl[1]))
        for y in range(tl[1], br[1] + 1):
            for x in range(tl[0], br[0] + 1):
                grid[y][x] = 0 if grid[y][x] == 1 else 1

    def adjust(state, tl, br):
        for y in range(tl[1], br[1] + 1):
            for x in range(tl[0], br[0] + 1):
                grid[y][x] += {0: -1, 1: 1}[state]
                if grid[y][x] < 0:
                    grid[y][x] = 0

    def boost(tl, br):
        for y in range(tl[1], br[1] + 1):
            for x in range(tl[0], br[0] + 1):
                grid[y][x] += 2

    # p1
    for i in inputs:
        bits = i.split()
        if bits[0] == 'turn':
            turn({'on': 1, 'off': 0}[bits[1]], coord(bits[2]), coord(bits[4]))
        elif bits[0] == 'toggle':
            toggle(coord(bits[1]), coord(bits[3]))

    print(sum(map(sum, grid)))

    # p2
    turn(0, [0,0], [999,999])
    #print(sum(map(sum, grid)))

    for i in inputs:
        bits = i.split()
        if bits[0] == 'turn':
            adjust({'on': 1, 'off': 0}[bits[1]], coord(bits[2]), coord(bits[4]))
        elif bits[0] == 'toggle':
            boost(coord(bits[1]), coord(bits[3]))

    print(sum(map(sum, grid)))
