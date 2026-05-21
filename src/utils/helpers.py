"""
utils/helpers.py
----------------
Core helper functions shared across all algorithms.
"""

import sys
sys.setrecursionlimit(200_000)

# 4-directional movement: up, down, left, right
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_valid(pos, maze):
    """Check if a position is within bounds and not a wall."""
    r, c = pos
    rows, cols = len(maze), len(maze[0])
    return 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0


def get_neighbors(pos, maze):
    """Yield all valid neighboring positions (4-directional)."""
    r, c = pos
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if is_valid((nr, nc), maze):
            yield (nr, nc)


def reconstruct_path(came_from, current):
    """Reconstruct path from start to current using came_from map."""
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path


def manhattan(a, b):
    """Manhattan distance heuristic between two grid positions."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
