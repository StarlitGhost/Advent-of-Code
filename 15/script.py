import sys
import math

inputs = (line.rstrip('\n') for line in open(sys.argv[1]))

pairs = []

for line in inputs:
    sensor, beacon = line.split(': closest beacon is at ')
    sensor = sensor[10:].split(', y=')
    sensor = (int(sensor[0][2:]), int(sensor[1]))
    beacon = beacon[2:].split(', y=')
    beacon = (int(beacon[0]), int(beacon[1]))
    pairs.append((sensor, beacon))

def mh_distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)

def dot(left, right):
    return sum(l*r for l,r in zip(left, right))

def add(left, right):
    return tuple(l + r for l, r in zip(left, right))

def mul(vec, scalar):
    return tuple(v * scalar for v in vec)

def to_int(vec):
    return tuple(int(math.floor(v) if v < 0 else math.ceil(v)) for v in vec)

def ray_circle_intersection(ray_start, ray_dir, circle_center, circle_radius):
    #print(circle_center, circle_radius)

    L = (circle_center[0] - ray_start[0], circle_center[1] - ray_start[1])
    tca = dot(L, ray_dir)
    d2 = dot(L, L) - tca**2
    if d2 > circle_radius**2:
        return None
    thc = math.sqrt(circle_radius**2 - d2)
    t0 = add(ray_start, mul(ray_dir, tca - thc))
    t1 = add(ray_start, mul(ray_dir, tca + thc))
    return t0, t1

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

covered = set()
beacons = set(beacon for _, beacon in pairs)
for sensor, beacon in pairs:
    ray_start = (0,int(sys.argv[2]))
    ray_dir = (1,0)
    radius = mh_distance(sensor, beacon)+1
    intersects = ray_circle_intersection(ray_start, ray_dir, sensor, radius)
    if intersects:
        #print(intersects)
        t0, t1 = intersects
        t0 = to_int(t0)
        t1 = to_int(t1)
        #print((t0, t1))
        points = walk(t0, t1)
        #print(points)
        for point in points:
            if mh_distance(sensor, point) < radius:
                covered.add(point)

covered -= beacons

print(len(covered))#, covered)
