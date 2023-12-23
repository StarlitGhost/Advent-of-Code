import sys
import pprint

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    graph = {}
    for line in inputs:
        places, distance = line.split(' = ')
        distance = int(distance)
        start, end = places.split(' to ')
        if start not in graph:
            graph[start] = {end: distance}
        else:
            graph[start][end] = distance
        if end not in graph:
            graph[end] = {start: distance}
        else:
            graph[end][start] = distance

    #pprint.pprint(graph)

    def find_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        paths = []
        for city in graph[start].keys():
            # only visit each city once
            if city not in path:
                newpaths = find_paths(graph, city, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def path_len(graph, path):
        path_len = 0
        # loop over adjacent city pairs in the path
        for start, dest in zip(path, path[1:]):
            path_len += graph[start][dest]
        return path_len

    shortest_path = None
    longest_path = None
    for start in graph.keys():
        for end in graph.keys():
            if start == end: continue

            paths = find_paths(graph, start, end)
            paths = list(filter(lambda l: len(l) == len(graph), paths))
            #pprint.pprint(paths)

            for path in paths:
                len_path = path_len(graph, path)
                if shortest_path is None or len_path < shortest_path:
                    shortest_path = len_path
                if longest_path is None or len_path > longest_path:
                    longest_path = len_path

    print(shortest_path)
    print(longest_path)
