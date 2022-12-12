with open('input') as f:
    inputs = (line.rstrip('\n') for line in f)

    forest = []
    visibility = []
    for line in inputs:
        forest.append([int(tree) for tree in line])
        visibility.append([0 for tree in line])

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

    #for line in visibility:
    #    print(''.join(map(str, line)))
    print(sum(map(sum, visibility)))
