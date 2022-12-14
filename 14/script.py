import sys
import itertools

inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

def pairwise(iterable):
    it = iter(iterable)
    a = next(it, None)
    for b in it:
        yield (a, b)
        a = b

def clamp1(n):
    return max(min(n, 1), -1)

class Grid:
    def __init__(self, chains):
        self.chains = []
        for chain in chains:
            self.chains.append([])
            links = chain.split(' -> ')
            for link in links:
                x, y = map(int, link.split(','))
                self.chains[-1].append((x, y))

        bounds = self.find_bounds()
        self.left, self.right, self.up, self.down = bounds
        self.width = self.right - self.left + 1
        self.height = self.down - self.up + 1

        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]

        self.build_walls()

        #self.grid[0][500-self.left] = 3

    def find_bounds(self):
        all_links = list(itertools.chain.from_iterable(self.chains))
        all_links.append((500,0))
        left = min(all_links, key=lambda link: link[0])[0]
        right = max(all_links, key=lambda link: link[0])[0]
        up = min(all_links, key=lambda link: link[1])[1]
        down = max(all_links, key=lambda link: link[1])[1]
        return left, right, up, down

    def build_walls(self):
        for chain in self.chains:
            self.build_wall(chain)

    def build_wall(self, chain):
        for start, end in pairwise(chain):
            dx = clamp1(end[0] - start[0])
            dy = clamp1(end[1] - start[1])
            x, y = start
            x -= self.left
            y -= self.up
            while (x+self.left, y+self.up) != (end[0]+dx, end[1]+dy):
                self.grid[y][x] = 1
                x += dx
                y += dy

    def char(self, cell):
        return {0: '.',
                1: '#',
                2: 'o',
                3: '+'}[cell]

    def __repr__(self):
        return '\n'.join(''.join(map(self.char, row)) for row in self.grid)

    def cell(self, coord):
        x, y = coord
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            return -1

    def below(self, x, y):
        x -= self.left
        y -= self.up
        search = [(x, y+1), (x-1, y+1), (x+1, y+1)]
        search = [self.cell(coord) for coord in search]
        return search

    def write_sand(self, x, y):
        self.grid[y - self.up][x - self.left] = 2


grid = Grid(inputs)

def step(x, y):
    for i, d in enumerate(grid.below(x, y)):
        if d == 0:
            y += 1
            x += {0: 0, 1: -1, 2: 1}[i]
            return True, x, y
        elif d == -1:
            return None, x, y
    else:
        return False, x, y

def simulate():
    x, y = 500, 0
    falling = True
    while falling:
        falling, x, y = step(x, y)
        if falling == False:
            grid.write_sand(x, y)
            x, y = 500, 0
            return True
        elif falling is None:
            return False

while simulate():
    pass

print(grid)

print(sum(row.count(2) for row in grid.grid))
