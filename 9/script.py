import sys

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    def extrapolate(values, reverse=False):
        e = [values]
        depth = 0
        while not all(v == 0 for v in e[-1]):
            e.append([second - first for first, second in zip(e[depth], e[depth][1:])])
            depth += 1
        if not reverse:
            e[-1].append(0)
        else:
            e[-1].insert(0, 0)
        while len(e) > 1:
            if not reverse:
                e[-2].append(e[-2][-1] + e[-1][-1])
            else:
                e[-2].insert(0, e[-2][0] - e[-1][0])
            e.pop(-1)
        if not reverse:
            return e[-1][-1]
        else:
            return e[-1][0]

    extrapolated = []
    for line in inputs:
        values = list(map(int, line.split()))
        extrapolated.append(extrapolate(values, reverse=False))
    print(sum(extrapolated))

    extrapolated = []
    for line in inputs:
        values = list(map(int, line.split()))
        extrapolated.append(extrapolate(values, reverse=True))
    print(sum(extrapolated))
