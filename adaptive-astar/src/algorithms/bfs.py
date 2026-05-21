"""
algorithms/bfs.py
-----------------
Breadth-First Search (BFS) for maze path planning.
Guarantees shortest path in unweighted grids.
"""

from collections import deque
from src.utils.helpers import is_valid, get_neighbors, reconstruct_path


def bfs(maze, start, goal):
    """
    Breadth-First Search algorithm.

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

    queue     = deque([start])
    came_from = {start: None}
    explored  = set()

    while queue:
        current = queue.popleft()
        explored.add(current)

        if current == goal:
            return reconstruct_path(came_from, goal), explored, came_from

        for neigh in get_neighbors(current, maze):
            if neigh not in came_from:
                came_from[neigh] = current
                queue.append(neigh)

    return None, explored, came_from
