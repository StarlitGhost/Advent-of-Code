from GhostyUtils import aoc
from collections import defaultdict, Counter
import random


def bfs(components, start, end):
    visited = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        node = path[-1]
        if node == end:
            return path
        for new_node in components[node]:
            if new_node in visited:
                continue
            visited.add(new_node)
            frontier.append(path + [new_node])
    return visited


def main():
    components = defaultdict(set)
    for wires in aoc.read_lines():
        comp, connections = wires.split(': ')
        components[comp].update(connections.split())
        for other_comp in components[comp]:
            components[other_comp].add(comp)

    seen = Counter()
    for _ in range(1000):
        comps = random.sample(list(components.keys()), 2)
        path = bfs(components, comps[0], comps[1])
        seen.update(tuple(sorted(link)) for link in zip(path, path[1:]))
    snips = seen.most_common(3)
    for snip in snips:
        l, r = snip[0]
        components[l].remove(r)
        components[r].remove(l)
    one = bfs(components, snips[0][0][0], None)
    two = bfs(components, snips[0][0][1], None)
    print('p1:', len(one) * len(two), f'| one: {len(one)} two: {len(two)}')


if __name__ == "__main__":
    main()
