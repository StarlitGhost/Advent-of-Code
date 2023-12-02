import sys
import functools

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    bag = {'red': 12, 'green': 13, 'blue': 14}
    possible_games = []
    powers = []
    for game in inputs:
        cols = {'red': 0, 'green': 0, 'blue': 0}
        skip = False

        g = game.split(':')
        game_id = int(g[0].split(' ')[1])
        rounds = g[1].split('; ')

        print(game, '->', game_id, rounds)

        for game_round in rounds:
            cubes = game_round.strip().split(', ')

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

        powers.append(functools.reduce(lambda x, y: x*y, cols.values()))

        if not skip:
            possible_games.append(game_id)

    print(sum(possible_games))
    print(sum(powers))
