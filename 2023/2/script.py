from math import prod
from GhostyUtils import aoc

if __name__ == '__main__':
    inputs = aoc.read_lines()

    bag = {'red': 12, 'green': 13, 'blue': 14}
    possible_games = []
    powers = []
    for game in inputs:
        cols = {'red': 0, 'green': 0, 'blue': 0}
        skip = False

        g = game.split(': ')
        game_id = int(g[0].split(' ')[1])
        rounds = g[1].split('; ')

        # print(game, '->', game_id, rounds)

        for game_round in rounds:
            cubes = game_round.split(', ')

            for cube in cubes:
                cube = cube.split(' ')

                num_cubes = int(cube[0])
                colour = cube[1]

                if cols[colour] < num_cubes:
                    cols[colour] = num_cubes

        for c, n in cols.items():
            if n > bag[c]:
                skip = True
                break

        powers.append(prod(cols.values()))

        if not skip:
            possible_games.append(game_id)

    print(sum(possible_games))
    print(sum(powers))
