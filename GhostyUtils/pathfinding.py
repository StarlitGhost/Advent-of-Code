from GhostyUtils.vec2 import Vec2, manhattan_distance
import heapq
from typing import Callable


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def empty(self):
        return not self.queue

    def put(self, item, priority):
        heapq.heappush(self.queue, (priority, item))

    def get(self):
        return heapq.heappop(self.queue)[1]


def a_star(start: Vec2, end: Vec2, *,
           neighbours: Callable,
           cost: Callable = None,
           heuristic: Callable = None,
           early_out: Callable = None) -> tuple[dict[Vec2, Vec2], dict[Vec2, int], Vec2]:

    if cost is None:
        cost = (lambda current_pos, next_pos: 1)
    if heuristic is None:
        heuristic = manhattan_distance
    if early_out is None:
        early_out = (lambda current_pos: False)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current_pos = frontier.get()

        if current_pos == end:
            break

        if early_out(current_pos):
            break

        for next_pos in neighbours(current_pos):
            new_cost = cost_so_far[current_pos] + cost(current_pos, next_pos)

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos, end)
                frontier.put(next_pos, priority)
                came_from[next_pos] = current_pos

    return came_from, cost_so_far, current_pos
