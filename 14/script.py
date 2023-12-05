import sys
from pprint import pprint


def calculate(reindeer, race_time):
    distances = {}
    for name, stats in reindeer.items():
        dist_per_rest = stats['speed'] * stats['duration']
        seconds_per_rest = stats['duration'] + stats['rest']
        remainder = race_time % seconds_per_rest
        cycles = race_time // seconds_per_rest
        distances[name] = dist_per_rest * cycles
        if remainder < stats['duration']:
            distances[name] += stats['speed'] * remainder
        else:
            distances[name] += dist_per_rest
    return distances

def score(reindeer, race_time):
    scores = {name: 0 for name in reindeer}
    for second in range(1, race_time):
        distances = calculate(reindeer, second)
        furthest = max(distances.values())
        furthest = [name for name, dist in distances.items() if dist == furthest]
        for name in furthest:
            scores[name] += 1
    return scores


if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    reindeer = {}
    for line in inputs:
        deer, rest = line.split(' seconds, but then must rest for ')
        rest = rest.split()[0]
        deer, speed = deer.split(' can fly ')
        speed, duration = speed.split(' km/s for ')
        reindeer[deer] = {'speed': int(speed),
                          'duration': int(duration),
                          'rest': int(rest)}

    race_time = 2503

    # p1
    distances = calculate(reindeer, race_time)
    #pprint(distances)
    print(max(distances.values()))

    # p2
    scores = score(reindeer, race_time)
    #pprint(scores)
    print(max(scores.values()))
