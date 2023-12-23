from GhostyUtils import aoc


class Mapping:
    def __init__(self, mapping):
        lines = mapping.split('\n')
        name = lines.pop(0).split()[0]
        self.src_name, _, self.dst_name = name.split('-')
        self.ranges = []
        for line in lines:
            dst_start, src_start, length = map(int, line.split())
            self.ranges.append((src_start, dst_start, length))
        self.ranges.sort()
        # print(name, self.ranges)

    def __repr__(self):
        return str(self.__dict__)

    def map_naive(self, source):
        for r in self.ranges:
            if r[0] <= source < r[0] + r[2]:
                return source-r[0]+r[1]
        return source


def read_mappings(inputs):
    mappings = []

    for mapping in inputs:
        mappings.append(Mapping(mapping))
    return mappings


def process_mappings(seed, mappings):
    conversions = [seed]
    for mapping in mappings:
        seed = mapping.map_naive(seed)
        conversions.append(seed)
    # print(seed, conversions)
    return seed


def process_ranges(seed_ranges, mappings):
    positions = sorted(seed_ranges)

    for mapping in mappings:
        ranges = list(mapping.ranges)
        new_positions = []

        while positions and ranges:
            pos_start, pos_len = positions[0]
            src_start, dst_start, range_len = ranges[0]
            pos_end = pos_start + pos_len
            src_end = src_start + range_len

            # before range, pass through
            if pos_end <= src_start:
                new_positions.append((pos_start, pos_len))
                positions.pop(0)
                continue
            # overlap range start, split
            if pos_start < src_start:
                new_len = src_start - pos_start
                new_positions.append((pos_start, new_len))
                positions[0] = (src_start, pos_len - new_len)
                continue
            # inside range, do mapping
            if pos_end <= src_end:
                new_positions.append((dst_start + pos_start - src_start, pos_len))
                positions.pop(0)
                continue
            # overlap range end, split and do mapping
            if pos_start < src_end:
                new_len = src_end - pos_start
                new_positions.append((dst_start + pos_start - src_start, new_len))
                positions[0] = (src_end, pos_len - new_len)
                continue

            # after range, skip
            ranges.pop(0)

        new_positions += positions

        new_positions.sort()
        positions = new_positions

    return positions


if __name__ == '__main__':
    inputs = aoc.read_sections()

    seeds = list(map(int, inputs.pop(0).split()[1:]))
    s = iter(seeds)
    seed_ranges = zip(s, s)

    mappings = read_mappings(inputs)
    locations = []
    for seed in seeds:
        locations.append(process_mappings(seed, mappings))
    print(min(locations))

    positions = process_ranges(seed_ranges, mappings)
    print(min(start for start, _ in positions))
