from GhostyUtils.vec2 import manhattan_distance
import heapq
from typing import Callable, Union


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def empty(self):
        return not self.queue

    def put(self, item, priority):
        heapq.heappush(self.queue, (priority, item))

    def get(self):
        return heapq.heappop(self.queue)[1]

    def __len__(self):
        return len(self.queue)


def a_star(start: tuple, end: tuple, *,
           neighbours: Callable = None,
           cost: Callable = None,
           heuristic: Callable = None,
           early_out: Callable = None) -> tuple[dict[tuple, tuple], dict[tuple, int], tuple]:

    if neighbours is None:
        raise ValueError("a_star: neighbours func is a required argument")
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

    while frontier:
        current_pos = frontier.get()

        if current_pos == end or early_out(current_pos):
            break

        for next_pos in neighbours(current_pos):
            new_cost = cost_so_far[current_pos] + cost(current_pos, next_pos)

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos, end)
                frontier.put(next_pos, priority)
                came_from[next_pos] = current_pos

    return came_from, cost_so_far, current_pos


def bfs(start: tuple, end: tuple, *,
        all_paths: bool = False,
        neighbours: Callable = None,
        early_out: Callable = None) -> Union[list[tuple], list[list[tuple]]]:

    if neighbours is None:
        raise ValueError("bfs: neighbours func is a required argument")
    if early_out is None:
        early_out = (lambda current_pos: False)

    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        current_pos = path[-1]

        if current_pos == end or early_out(current_pos):
            if all_paths:
                yield path
                continue
            else:
                yield path

        for next_pos in neighbours(current_pos):
            if next_pos in path:
                continue

            new_path = list(path)
            new_path.append(next_pos)
            frontier.append(new_path)

    return


def dfs(start: tuple, end: tuple, *,
        all_paths: bool = False,
        neighbours: Callable = None,
        early_out: Callable = None) -> Union[list[tuple], list[list[tuple]]]:

    if neighbours is None:
        raise ValueError("dfs: neighbours func is a required argument")
    if early_out is None:
        early_out = (lambda current_pos: False)

    frontier = [[start]]
    while frontier:
        path = frontier.pop()
        current_pos = path[-1]

        if current_pos == end or early_out(current_pos):
            if all_paths:
                yield path
                continue
            else:
                yield path

        for next_pos in neighbours(current_pos):
            if next_pos in path:
                continue

            new_path = list(path)
            new_path.append(next_pos)
            frontier.append(new_path)

    return


def reconstruct_path(came_from, start, end):
    current_pos = end
    path = []
    if end not in came_from:
        return []

    while current_pos != start:
        path.append(current_pos)
        current_pos = came_from[current_pos]

    path.append(start)
    path.reverse()
    return path
