import math

with open('input') as f:
    inputs = (line.rstrip('\n') for line in f)

    forest = []
    visibility = []
    scenic = []
    for line in inputs:
        forest.append([int(tree) for tree in line])
        visibility.append([0 for tree in line])
        scenic.append([0 for tree in line])

    def cast_ray(direction, start, forest, visibility):
        height = -1
        if direction in ['left', 'right']:
            d = direction == 'right'
            from_ = 0 if d else len(forest[start]) - 1
            to = len(forest[start]) if d else 0
            step = 1 if d else -1
            for x in range(from_, to, step):
                if forest[start][x] > height:
                    visibility[start][x] = 1
                    height = forest[start][x]
        elif direction in ['up', 'down']:
            d = direction == 'down'
            from_ = 0 if d else len(forest) - 1
            to = len(forest) if d else 0
            step = 1 if d else -1
            for y in range(from_, to, step):
                if forest[y][start] > height:
                    visibility[y][start] = 1
                    height = forest[y][start]

    def cast_rays(forest, visibility):
        for y in range(0, len(forest)):
            cast_ray('right', y, forest, visibility)
            cast_ray('left', y, forest, visibility)
        for x in range(0, len(forest[0])):
            cast_ray('down', x, forest, visibility)
            cast_ray('up', x, forest, visibility)

    cast_rays(forest, visibility)

    def print_map(map_):
        for line in map_:
            print(''.join(map(str, line)))

    #print_map(visibility)
    print(sum(map(sum, visibility)))

    def scenic_distance(x, y, d):
        distance = 0
        cur_x = x+d[0]
        cur_y = y+d[1]
        while 0 <= cur_x < len(forest[0]) and 0 <= cur_y < len(forest):
            distance += 1
            if forest[x][y] <= forest[cur_x][cur_y]:
                break
            cur_x += d[0]
            cur_y += d[1]
        return distance

    def cast_scenic_rays(x, y):
        sd = []
        for d in [(-1,0), (1,0), (0,-1), (0,1)]:
            sd.append(scenic_distance(x, y, d))
        return sd

    max_scenic = 0
    for y in range(0, len(forest)):
        for x in range(0, len(forest[y])):
            scenic[y][x] = cast_scenic_rays(x, y)
            if math.prod(scenic[y][x]) > max_scenic:
                max_scenic = math.prod(scenic[y][x])
                print(x, y, scenic[y][x], max_scenic)
