import sys

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    def extrapolate(values):
        e = [values]
        while any(e[-1]):
            e.append([second - first for first, second in zip(e[-1], e[-1][1:])])
        while len(e) > 1:
            e[-2].append(e[-2][-1] + e[-1][-1])
            e.pop(-1)
        return e[-1][-1]

    values = [list(map(int, line.split())) for line in inputs]

    print(sum(extrapolate(v) for v in values))
    print(sum(extrapolate(list(reversed(v))) for v in values))
