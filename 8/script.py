import sys
import math

if __name__ == '__main__':
    directions, nodes = open(sys.argv[1]).read().strip().split('\n\n')
    nodes = nodes.split('\n')

    graph = {}
    for node in nodes:
        label, connections = node.split(' = ')
        graph[label] = connections[1:-1].split(', ')

    def navigate(count):
        return 'LR'.index(directions[count % len(directions)])

    node = 'AAA'
    count = 0
    while node != 'ZZZ':
        if 'AAA' not in graph or 'ZZZ' not in graph:
            break
        node = graph[node][navigate(count)]
        count += 1
    print(count)

    nodes = list(filter(lambda n: n.endswith('A'), graph))
    paths = [{'start': node, 'period': 0} for node in nodes]
    count = 0
    while not all(path['period'] != 0 for path in paths):
        for i, node in enumerate(nodes):
            if node.endswith('Z'):
                if paths[i]['period'] == 0:
                    paths[i]['period'] = count
            nodes[i] = graph[node][navigate(count)]
        count += 1

    print(math.lcm(*(path['period'] for path in paths)))
