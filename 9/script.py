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

    extrapolated = []
    for line in inputs:
        values = list(map(int, line.split()))
        extrapolated.append(extrapolate(values))
    print(sum(extrapolated))

    extrapolated = []
    for line in inputs:
        values = list(map(int, line.split()))
        extrapolated.append(extrapolate(list(reversed(values))))
    print(sum(extrapolated))
