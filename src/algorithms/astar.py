"""
algorithms/astar.py
-------------------
A* Search with Manhattan distance heuristic.
Optimal and more efficient than BFS for grid mazes.
"""

import heapq
import itertools
from src.utils.helpers import is_valid, get_neighbors, reconstruct_path, manhattan


def astar(maze, start, goal):
    """
    A* Search algorithm using Manhattan distance heuristic.

    Parameters
    ----------
    maze  : 2D list of int  (0 = free, 1 = wall)
    start : (row, col) tuple
    goal  : (row, col) tuple

    Returns
    -------
    path     : list of (row, col) from start to goal, or None
    explored : set of explored positions
    came_from: dict mapping position -> parent position
    """
    if not is_valid(start, maze) or not is_valid(goal, maze):
        return None, set(), {}

    counter   = itertools.count()          # tiebreaker for stable heap ordering
    open_heap = []
    heapq.heappush(open_heap, (manhattan(start, goal), 0, next(counter), start))

    came_from = {start: None}
    g_score   = {start: 0}
    explored  = set()

    while open_heap:
        _, current_g, _, current = heapq.heappop(open_heap)

        if current in explored:
            continue
        explored.add(current)

        if current == goal:
            return reconstruct_path(came_from, goal), explored, came_from

        for neigh in get_neighbors(current, maze):
            if neigh in explored:
                continue
            tentative_g = current_g + 1
            if tentative_g < g_score.get(neigh, float("inf")):
                g_score[neigh]   = tentative_g
                came_from[neigh] = current
                f = tentative_g + manhattan(neigh, goal)
                heapq.heappush(open_heap, (f, tentative_g, next(counter), neigh))

    return None, explored, came_from
