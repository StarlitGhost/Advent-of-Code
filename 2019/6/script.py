from GhostyUtils import aoc
from collections import defaultdict


def bfs(graph, start, end):
    visited = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        node = path[-1]
        if node == end:
            return path

        for new_node in graph[node]:
            if new_node in visited:
                continue
            frontier.append(path + [new_node])
            visited.add(new_node)


def main():
    orbits = defaultdict(set)
    satellites = set()
    for orbit in aoc.read_lines():
        body, satellite = orbit.split(')')
        orbits[body].add(satellite)
        orbits[satellite].add(body)
        satellites.add(satellite)

    total_orbits = 0
    for satellite in satellites:
        path = bfs(orbits, 'COM', satellite)
        total_orbits += len(path) - 1
    print('p1:', total_orbits)

    path = bfs(orbits, 'YOU', 'SAN')
    print('p2:', len(path)-2-1)


if __name__ == "__main__":
    main()
