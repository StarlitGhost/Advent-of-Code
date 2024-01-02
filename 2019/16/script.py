from GhostyUtils import aoc
from itertools import accumulate, cycle


def fft(signal: list[int]) -> list[int]:
    pattern = [0, 1, 0, -1]
    output = [s for s in signal]
    for _ in range(100):
        for o in range(len(output)):
            out = 0
            for i, n in enumerate(output):
                mul = pattern[((i + 1) // (o + 1)) % len(pattern)]
                out += n * mul
            output[o] = abs(out) % 10
    return ''.join(str(s) for s in output[:8])


def fast_fft(signal: list[int], offset: int) -> list[int]:
    # offset is > len/2, so everything up to offset is multiplied by 0,
    # and everything after by 1.
    # so each output digit is just (sum of the following digits % 10)
    offset_len = len(signal) * 10000 - offset
    looped_signal = cycle(signal[::-1])
    partial_signal = [next(looped_signal) for _ in range(offset_len)]
    for _ in range(100):
        partial_signal = [n % 10 for n in accumulate(partial_signal)]
    return ''.join(str(n) for n in partial_signal[-1:-9:-1])


def main():
    input_str = aoc.read()
    signal = [int(n) for n in input_str]

    output = fft(signal)
    print('p1:', output)

    offset = int(input_str[:7])
    output = fast_fft(signal, offset)
    print('p2:', output)


if __name__ == "__main__":
    main()
