from math import prod
from GhostyUtils import aoc

if __name__ == '__main__':
    inputs = aoc.read_lines()

    times = map(int, inputs[0].split()[1:])
    distances = map(int, inputs[1].split()[1:])

    races = zip(times, distances)

    def calc_holds(races):
        hold_winners = []
        for time, distance in races:
            for hold in range(1, time//2):
                d = (time-hold)*hold
                # found lowest winning hold
                if d > distance:
                    # highest is time-hold, winning range is (time-hold)-hold+1
                    hold_winners.append((time-hold)-hold+1)
                    break
        return hold_winners

    print(prod(calc_holds(races)))

    time = int(''.join(inputs[0].split()[1:]))
    distance = int(''.join(inputs[1].split()[1:]))
    races = [(time, distance)]
    print(prod(calc_holds(races)))
