import sys

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))
    inputs = next(inputs)

    p1_santa = [0, 0]
    santas = [[0, 0], [0, 0]]
    p1_grid = {}
    p2_grid = {}

    # add a present to the starting house
    p1_grid[tuple(p1_santa)] = 1
    p2_grid[tuple(santas[0])] = 1

    for santa, dir in enumerate(inputs):
        move = {'>': [1, 0], '<': [-1, 0], '^': [0, 1], 'v': [0, -1]}[dir]

        # p1
        p1_santa = [sum(x) for x in zip(p1_santa, move)]
        house = tuple(p1_santa)
        if house not in p1_grid:
            p1_grid[house] = 1
        else:
            p1_grid[house] += 1

        # p2
        santas[santa % 2] = [sum(x) for x in zip(santas[santa % 2], move)]
        house = tuple(santas[santa % 2])
        if house not in p2_grid:
            p2_grid[house] = 1
        else:
            p2_grid[house] += 1

    print(len(p1_grid), len(p2_grid))
