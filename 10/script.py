import sys

def process_seq(seq):
    n = 1
    prev = None
    new_seq = []
    for c in seq:
        if c == prev:
            n += 1
        elif prev is not None:
            new_seq.extend([f'{n}', f'{prev}'])
            n = 1
        prev = c
    new_seq.extend([str(n), str(prev)])
    return new_seq

if __name__ == '__main__':
    inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

    # p1
    seq = list(*inputs)
    for i in range(40):
        seq = process_seq(seq)
    print(len(seq))

    # p2
    seq = list(*inputs)
    for i in range(50):
        seq = process_seq(seq)
    print(len(seq))
