import sys


class Mapping:
    def __init__(self, inputs):
        self.name = next(inputs)
        self.ranges = []
        reading = True
        while True:
            r = next(inputs)
            if not r:
                return
            else:
                self.ranges.append([int(num) for num in r.split()])

    def __repr__(self):
        return str(self.__dict__)

    def map(self, source):
        for r in self.ranges:
            if r[1] <= source <= r[1] + r[2]:
                return source-r[1]+r[0]
        return source

def read_mappings(inputs):
    mappings = []

    try:
        while True:
            mappings.append(Mapping(inputs))
    except StopIteration:
        return mappings

def process_mappings(seed, mappings):
    conversions = [seed]
    for mapping in mappings:
        seed = mapping.map(seed)
        conversions.append(seed)
    #print(seed, conversions)
    return seed

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    seeds = [int(s) for s in next(inputs).lstrip('seeds: ').split()]
    next(inputs)

    mappings = read_mappings(inputs)
    locations = []
    for seed in seeds:
        locations.append(process_mappings(seed, mappings))
    print(min(locations))

    lowest_location = None
    for i in range(0, len(seeds), 2):
        for seed in range(seeds[i], seeds[i]+seeds[i+1]):
            loc = process_mappings(seed, mappings)
            if lowest_location is None or loc < lowest_location:
                lowest_location = loc
    print(lowest_location)

