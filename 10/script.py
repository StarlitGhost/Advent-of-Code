import sys
from enum import Enum
import functools
from GhostyUtils.grid import Grid
from GhostyUtils.vec2 import Vec2

class Dir(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

dir_offset = {Dir.WEST: Vec2(-1,0),
              Dir.EAST: Vec2(1,0),
              Dir.NORTH: Vec2(0,-1),
              Dir.SOUTH: Vec2(0,1)}

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
    pipe_grid = Grid(rows)
    width = pipe_grid.width()
    height = pipe_grid.height()

    def s_type(grid, s_pos):
        dirs = [dir_ for dir_ in pipe_connects['S']
                if dir_connects[dir_] in pipe_connects[grid[s_pos + dir_offset[dir_]]]]
        return [pipe for pipe, pipe_dirs in pipe_connects.items() if pipe_dirs == dirs][0]

    def find_path(grid, s_pos):
        pos = s_pos
        path = [s_pos]
        came_from = None
        done = False
        while not done:
            # filter out the direction we came from, we can't go backwards
            search_dirs = [dir_ for dir_ in pipe_connects[grid[pos]] if dir_ != came_from]
            for dir_ in search_dirs:
                # get the pipe in the direction we're searching
                pipe = grid[pos + dir_offset[dir_]]
                # if it's S, we're done
                if pipe == 'S':
                    done = True
                    break
                # if the pipe we're looking at connects to our current position, move to that pipe
                if dir_connects[dir_] in pipe_connects[pipe]:
                    pos = pos + dir_offset[dir_]
                    path.append(pos)
                    came_from = dir_connects[dir_]
                    break
        return path

    s_pos = pipe_grid.find('S')
    path = find_path(pipe_grid, s_pos)
    print(len(path) // 2)


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
                    '.F-',
                    '.|.'],
              '.': ['...',
                    '...',
                    '...']}
    big_width = width*3
    big_height = height*3
    big_grid = Grid([['.' for _ in range(big_width)] for _ in range(big_height)])
    s_pipe = s_type(pipe_grid, s_pos)
    for y, row in enumerate(pipe_grid.by_rows()):
        for x, pipe in enumerate(row):
            for by in range(3):
                for bx in range(3):
                    big_grid[x*3+bx,y*3+by] = expand[pipe if pipe != 'S' else s_pipe][by][bx]
            if pipe == 'S':
                big_grid[x*3+1,y*3+1] = 'S'
    #print(big_grid)
    #print()
    big_s_pos = big_grid.find('S')
    big_path = find_path(big_grid, big_s_pos)
    
    for pos in big_path:
        big_grid[pos] = '@'
    #print(big_grid)

    def inside(pos, *, grid, fill, path):
        if pos in path:
            return False
        if not grid.vec2_inside(pos):
            return False
        if grid[pos] == fill:
            return False
        return True
    inside_func = functools.partial(inside, grid=big_grid, path=big_path, fill='#')
    fillcoords = [(0,0),(width-1,0),(width-1,height-1),(0,height-1)]
    for pos in fillcoords:
        big_grid.flood_fill(pos, '#', inside_func)

    #print(big_grid)
    smol_grid = Grid([[pipe for pipe in row[1::3]] for row in big_grid[1::3]])
    #print(smol_grid)
    print(sum(sum(1 for pipe in row if pipe not in '@#') for row in smol_grid))
