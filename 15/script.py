import sys

def mh_distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)

def clamp1(n):
    return max(min(n, 1), -1)

def walk(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = clamp1(x2 - x1)
    dy = clamp1(y2 - y1)

    x, y = x1, y1
    points = []
    if dx == 0 and dy == 0:
        points.append(start)
    while (x, y) != (x2+dx, y2+dy):
        points.append((x,y))
        x += dx
        y += dy
    return points

def row_sensor_intersection(row, sensor, mh_radius):
    if sensor[1]-mh_radius <= row <= sensor[1]+mh_radius:
        y_distance = abs(sensor[1]-row)
        depth = mh_radius - y_distance
        start_x = sensor[0] - depth
        end_x = sensor[0] + depth
        return (start_x, row), (end_x, row)
    return None

def scan(row, pairs):
    intersections = []
    for sensor, beacon in pairs:
        radius = mh_distance(sensor, beacon)
        intersects = row_sensor_intersection(row, sensor, radius)
        if intersects:
            t0, t1 = intersects
            intersections.append(intersects)
    return intersections

def row_coverage(intersections):
    covered = set()
    for i in intersections:
        points = walk(i[0], i[1])
        covered.update(points)
    return covered

if __name__ == '__main__':
    inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

    pairs = []

    for line in inputs:
        sensor, beacon = line.split(': closest beacon is at ')
        sensor = sensor[10:].split(', y=')
        sensor = (int(sensor[0][2:]), int(sensor[1]))
        beacon = beacon[2:].split(', y=')
        beacon = (int(beacon[0]), int(beacon[1]))
        pairs.append((sensor, beacon))

    from timeit import default_timer as timer
    start = timer()

    beacons = set(b for _, b in pairs)
    intersections = scan(int(sys.argv[2]), pairs)
    covered = row_coverage(intersections)
    covered -= beacons

    end = timer()

    print(f'part 1: {len(covered)} {end-start:.6f} seconds')

    max_coord = int(sys.argv[3])

    start = timer()

    for y in range(0,max_coord+1):
        intersections = scan(y, pairs)
        x = 0
        while x <= max_coord:
            no_intersections = True
            for i in intersections:
                if i[0][0] <= x <= i[1][0]:
                    no_intersections = False
                    x = i[1][0] + 1
            if no_intersections:
                end = timer()
                print(f'part 2: {(x,y)} {x*4000000 + y} {end-start:.6f} seconds')
                exit()
