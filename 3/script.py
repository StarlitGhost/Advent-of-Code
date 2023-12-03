import sys

def search(grid, x, y):
    width = len(grid[0])
    height = len(grid)

    for search_y in [-1,0,1]:
        if y + search_y < 0 or y + search_y > height-1:
            continue

        for search_x in [-1,0,1]:
            if x + search_x < 0 or x + search_x > width-1:
                continue
            search = grid[y + search_y][x + search_x]
            if isinstance(search, int):
                continue
            elif search == '.':
                continue
            else:
                return True
    return False


if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    grid = [[c for c in line] for line in inputs]
    for y in range(len(grid)):
        num = ''
        for x in range(len(grid[y])):
            if grid[y][x].isnumeric():
                num += grid[y][x]
            else:
                if num:
                    for c in range(len(num)):
                        grid[y][x-c-1] = int(num)
                    num = ''
        if num:
            for c in range(len(num)):
                grid[y][len(grid[y])-c-1] = int(num)
            num = ''
                
    parts = []
    for y in range(len(grid)):
        searching = True
        line_parts = []
        for x in range(len(grid[y])):
            if isinstance(grid[y][x], int):
                if searching:
                    if search(grid, x, y):
                        parts.append(grid[y][x])
                        line_parts.append(grid[y][x])
                        searching = False
            else:
                searching = True

        #print(y, line_parts)

    print(sum(parts))
