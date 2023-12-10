import sys
from enum import Enum

class Dir(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

dir_offset = {Dir.WEST: (-1,0),
              Dir.EAST: (1,0),
              Dir.NORTH: (0,-1),
              Dir.SOUTH: (0,1)}

pipe_connects = {'|': [Dir.NORTH, Dir.SOUTH],
                 '-': [Dir.EAST, Dir.WEST],
                 'L': [Dir.NORTH, Dir.EAST],
                 'J': [Dir.NORTH, Dir.WEST],
                 '7': [Dir.SOUTH, Dir.WEST],
                 'F': [Dir.SOUTH, Dir.EAST],
                 '.': [],
                 'S': [Dir.NORTH, Dir.SOUTH, Dir.EAST, Dir.WEST]}

dir_connects = {Dir.NORTH: Dir.SOUTH,
                Dir.SOUTH: Dir.NORTH,
                Dir.EAST: Dir.WEST,
                Dir.WEST: Dir.EAST}


if __name__ == '__main__':
    rows = open(sys.argv[1]).read().strip().split('\n')
    pipe_grid = [[x for x in row] for row in rows]
    width = len(pipe_grid[0])
    height = len(pipe_grid)

    def find_s(grid):
        sy = [y for y, row in enumerate(grid) if 'S' in row][0]
        sx = grid[sy].index('S')
        return (sx, sy)

    def get_pipe(grid, pos, offset=(0,0)):
        return grid[pos[1]+offset[1]][pos[0]+offset[0]]

    def s_type(grid, s_pos):
        dirs = [dir_ for dir_ in pipe_connects['S']
                if dir_connects[dir_] in pipe_connects[get_pipe(grid, s_pos, dir_offset[dir_])]]
        return [pipe for pipe, pipe_dirs in pipe_connects.items() if pipe_dirs == dirs][0]

    def move(pos, offset):
        return (pos[0]+offset[0], pos[1]+offset[1])

    def find_path(grid, s_pos):
        pos = s_pos
        path = [s_pos]
        came_from = None
        done = False
        while not done:
            # filter out the direction we came from, we can't go backwards
            search_dirs = [dir_ for dir_ in pipe_connects[get_pipe(grid, pos)] if dir_ != came_from]
            for dir_ in search_dirs:
                # get the pipe in the direction we're searching
                pipe = get_pipe(grid, pos, dir_offset[dir_])
                # if it's S, we're done
                if pipe == 'S':
                    done = True
                    break
                # if the pipe we're looking at connects to our current position, move to that pipe
                if dir_connects[dir_] in pipe_connects[pipe]:
                    pos = move(pos, dir_offset[dir_])
                    path.append(pos)
                    came_from = dir_connects[dir_]
                    break
        return path

    def print_grid(grid):
        print('\n'.join(''.join(row) for row in grid))

    s_pos = find_s(pipe_grid)
    path = find_path(pipe_grid, s_pos)
    print(len(path) // 2)

    def inside(grid, pos, fill, path):
        if pos in path:
            return False
        in_width = 0 <= pos[0] < len(grid[0])
        in_height = 0 <= pos[1] < len(grid)
        if not in_width or not in_height:
            return False
        if get_pipe(grid, pos) == fill:
            return False
        return True

    def flood_fill(grid, pos, fill, path, inside=inside):
        if not inside(grid, pos, fill, path):
            return
        s = [(pos[0], pos[0], pos[1], 1), (pos[0], pos[0], pos[1] - 1, -1)]
        while s:
            x1, x2, y, dy = s.pop(0)
            x = x1
            if inside(grid, (x, y), fill, path):
                while inside(grid, (x - 1, y), fill, path):
                    grid[y][x-1] = fill
                    x -= 1
                if x < x1:
                    s.append((x, x1 - 1, y - dy, -dy))
            while x1 <= x2:
                while inside(grid, (x1, y), fill, path):
                    grid[y][x1] = fill
                    x1 += 1
                if x1 > x:
                    s.append((x, x1 - 1, y + dy, dy))
                if x1 - 1 > x2:
                    s.append((x2 + 1, x1 - 1, y - dy, -dy))
                x1 += 1
                while x1 < x2 and not inside(grid, (x1, y), fill, path):
                    x1 += 1
                x = x1

    expand = {'|': ['.|.',
                    '.|.',
                    '.|.'],
              '-': ['...',
                    '---',
                    '...'],
              'L': ['.|.',
                    '.L-',
                    '...'],
              'J': ['.|.',
                    '-J.',
                    '...'],
              '7': ['...',
                    '-7.',
                    '.|.'],
              'F': ['...',
                    ' F-',
                    '.|.'],
              '.': ['...',
                    '...',
                    '...']}
    big_width = width*3
    big_height = height*3
    big_grid = [['.' for _ in range(big_width)] for _ in range(big_height)]
    s_pipe = s_type(pipe_grid, s_pos)
    for y, row in enumerate(pipe_grid):
        for x, pipe in enumerate(row):
            for by in range(3):
                for bx in range(3):
                    big_grid[y*3+by][x*3+bx] = expand[pipe if pipe != 'S' else s_pipe][by][bx]
            if pipe == 'S':
                big_grid[y*3+1][x*3+1] = 'S'
    #print_grid(big_grid)
    #print()
    big_s_pos = find_s(big_grid)
    big_path = find_path(big_grid, big_s_pos)
    
    for pos in big_path:
        big_grid[pos[1]][pos[0]] = '@'
    #print_grid(big_grid)
    fillcoords = [(0,0),(width-1,0),(width-1,height-1),(0,height-1)]
    [flood_fill(big_grid, pos, '#', big_path) for pos in fillcoords]
    #print_grid(big_grid)
    smol_grid = [[pipe for pipe in row[1::3]] for row in big_grid[1::3]]
    print()
    print_grid(smol_grid)
    print(sum(sum(1 for pipe in row if pipe not in '@#') for row in smol_grid))
