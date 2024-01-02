from GhostyUtils import aoc


def fft(signal: list[int]) -> list[int]:
    pattern = [0, 1, 0, -1]
    output = []
    for o in range(len(signal)):
        out = 0
        for i, n in enumerate(signal):
            mul = pattern[((i + 1) // (o + 1)) % len(pattern)]
            out += n * mul
        output.append(abs(out) % 10)
    return output


def test() -> bool:
    data = [
        {'in': "12345678",
         'out': "48226158"},
    ]
    for d in data:
        input = [int(n) for n in d['in']]
        output = [int(n) for n in d['out']]
        assert fft(input) == output


def main():
    test()

    signal = [int(n) for n in aoc.read()]

    for _ in range(100):
        signal = fft(signal)
    print(''.join(str(s) for s in signal[:8]))


if __name__ == "__main__":
    main()
