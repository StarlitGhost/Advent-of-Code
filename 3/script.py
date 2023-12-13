import sys
from GhostyUtils.grid import Grid

def search(grid, x, y):
    width = grid.width()
    height = grid.height()

    for search_y in [-1,0,1]:
        if y + search_y < 0 or y + search_y > height-1:
            continue

        for search_x in [-1,0,1]:
            if x + search_x < 0 or x + search_x > width-1:
                continue
            search = grid[x + search_x, y + search_y]
            if isinstance(search, int):
                continue
            elif search == '.':
                continue
            else:
                return True
    return False

def search_gear(grid, x, y):
    width = grid.width()
    height = grid.height()

    part_nums = []
    for search_y in [-1,0,1]:
        if y + search_y < 0 or y + search_y > height-1:
            continue

        line_part_nums = []

        for search_x in [-1,0,1]:
            if x + search_x < 0 or x + search_x > width-1:
                continue
            search = grid[x + search_x, y + search_y]
            if isinstance(search, int) and search not in line_part_nums:
                 line_part_nums.append(search)

        part_nums.extend(line_part_nums)

    if len(part_nums) == 2:
        #print(part_nums, '->', part_nums[0] * part_nums[1])
        return part_nums[0] * part_nums[1]
    else:
        #print(part_nums, 'X')
        return 0

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    grid = Grid(inputs)

    # convert numbers in the grid into ints
    for y in range(grid.height()):
        num = ''
        for x in range(grid.width()):
            if grid[x,y].isnumeric():
                num += grid[x,y]
            else:
                if num:
                    for c in range(len(num)):
                        grid[x-c-1,y] = int(num)
                    num = ''
        # handle numbers on the end of a row
        if num:
            for c in range(len(num)):
                grid[grid.width()-c-1,y] = int(num)
            num = ''
        
    # p1
    parts = []
    for y in range(grid.height()):
        searching = True
        #line_parts = []
        for x in range(grid.width()):
            if isinstance(grid[x,y], int):
                if searching:
                    if search(grid, x, y):
                        parts.append(grid[x,y])
                        #line_parts.append(grid[x,y])
                        searching = False
            else:
                searching = True

        #print(y, line_parts)

    print(sum(parts))

    # p2
    gear_sum = 0
    for y in range(grid.height()):
        for x in range(grid.width()):
            if grid[x,y] != '*':
                continue
            
            gear_sum += search_gear(grid, x, y)

    print(gear_sum)
