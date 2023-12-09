import sys

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    def extrapolate(sequence):
        # d = derivative sequences
        d = [sequence]
        while any(d[-1]):
            d.append([second - first for first, second in zip(d[-1], d[-1][1:])])
        while len(d) > 1:
            d[-2].append(d[-2][-1] + d[-1][-1])
            d.pop(-1)
        return d[-1][-1]

    sequences = [list(map(int, line.split())) for line in inputs]

    print(sum(extrapolate(sequence) for sequence in sequences))
    print(sum(extrapolate(list(reversed(sequence))) for sequence in sequences))
