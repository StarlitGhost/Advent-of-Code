import sys
import itertools

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))
    jars = [int(i) for i in inputs]

    combos = []
    for i in range(1, len(jars)):
        combos.extend([combo for combo in itertools.combinations(jars, i) if sum(combo) == 150])

    # p1
    print(len(combos))
    
    # p2
    print(len(list(filter(lambda l: len(l) == len(combos[0]), combos))))
