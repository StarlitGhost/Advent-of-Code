import sys
from pprint import pprint


def simulate(reindeer, race_time):
    dist_per_rest = reindeer['speed'] * reindeer['duration']
    seconds_per_rest = reindeer['duration'] + reindeer['rest']
    remainder = race_time % seconds_per_rest
    cycles = race_time // seconds_per_rest
    distance = dist_per_rest * cycles
    if remainder < reindeer['duration']:
        distance += reindeer['speed'] * remainder
    else:
        distance += dist_per_rest
    return distance


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

    distances = {}
    for deer in reindeer:
        distances[deer] = simulate(reindeer[deer], 2503)
    #pprint(distances)
    print(max(distances.values()))
