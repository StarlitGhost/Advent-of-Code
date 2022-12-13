import sys
import heapq

inputs = [line.rstrip('\n') for line in open(sys.argv[1])]

class Cell:
    def __init__(self, char, x, y):
        self.x = x
        self.y = y

        self.start = False
        self.end = False
        if char == 'S':
            self.start = True
            char = 'a'
        elif char == 'E':
            self.end = True
            char = 'z'

        self.height = ord(char) - ord('a')

    def __lt__(self, other):
        return self.tuple() < other.tuple()

    def tuple(self):
        return (self.x, self.y)

    def __str__(self):
        if self.start:
            return 'S'
        elif self.end:
            return 'E'
        return chr(self.height + ord('a'))

class Terrain:
    def __init__(self, data):
        self.cells = [
                [Cell(char, x, y) for x, char in enumerate(row)]
                for y, row in enumerate(data)
                ]

    def __repr__(self):
        return '\n'.join(''.join((str(cell) for cell in row))
                for row in self.cells)

    def draw_with_path(self, path):
        return '\n'.join(''.join((str(cell) if cell not in path else '#' for cell in row))
                for row in self.cells)

    def find_start(self):
        for row in self.cells:
            for cell in row:
                if cell.start:
                    return cell

    def find_end(self):
        for row in self.cells:
            for cell in row:
                if cell.end:
                    return cell

    def in_bounds(self, coords):
        x, y = coords
        return 0 <= x < len(self.cells[0]) and 0 <= y < len(self.cells)

    def traversible(self, from_cell, to_cell):
        # we can only go up one height level at a time
        # we can go down as much as we like though!
        if to_cell.height - from_cell.height > 1:
            return False
        return True

    def neighbours(self, cell):
        x, y = cell.tuple()
        coords = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        coords = [c for c in coords if self.in_bounds(c)]
        neighbours = [self.cells[c[1]][c[0]] for c in coords]
        neighbours = [n for n in neighbours if self.traversible(cell, n)]
        return neighbours

    def cost(self, from_cell, to_cell):
        return 1#to_cell.height - from_cell.height

    def heuristic(self, cell, end):
        x1, y1 = cell.tuple()
        x2, y2 = end.tuple()
        return abs(x1 - x2) + abs(y1 - y2)


terrain = Terrain(inputs)
print(terrain)

start = terrain.find_start()
end = terrain.find_end()

print(f'Start: {start.tuple()} | End: {end.tuple()}')

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def empty(self):
        return not self.queue

    def put(self, item, priority):
        heapq.heappush(self.queue, (priority, item))

    def get(self):
        return heapq.heappop(self.queue)[1]

def a_star(terrain, start, end):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current_cell = frontier.get()

        if current_cell == end:
            break

        for next_cell in terrain.neighbours(current_cell):
            new_cost = cost_so_far[current_cell] + terrain.cost(current_cell, next_cell)

            if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                cost_so_far[next_cell] = new_cost
                priority = new_cost + terrain.heuristic(next_cell, end)
                frontier.put(next_cell, priority)
                came_from[next_cell] = current_cell

    return came_from, cost_so_far

def reconstruct_path(came_from, start, end):
    current_cell = end
    path = []
    if end not in came_from:
        return []

    while current_cell != start:
        path.append(current_cell)
        current_cell = came_from[current_cell]

    path.append(start)
    path.reverse()
    return path

came_from, cost_so_far = a_star(terrain, start, end)
path = reconstruct_path(came_from, start, end)
#print([cell.tuple() for cell in path])

print(terrain.draw_with_path(path))
print(len(path) - 1)
