import sys

if __name__ == '__main__':
    inputs = ''.join((line.rstrip('\n') for line in open(sys.argv[1])))

    char_map = {'(': 1, ')': -1}
    moves = [char_map[c] for c in inputs]
    floor = 0
    found = False
    for pos, move in enumerate(moves):
        floor += move

        if floor == -1 and not found:
            print(pos+1)
            found = True

    print(floor)
