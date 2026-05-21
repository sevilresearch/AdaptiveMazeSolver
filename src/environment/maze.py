"""
environment/maze.py
--------------------
Random maze generator that guarantees at least one valid path
from start (0,0) to goal (rows-1, cols-1).
"""

import random
from src.algorithms.bfs import bfs


def generate_multi_path_maze(rows, cols, wall_prob=0.25, seed=None):
    """
    Generate a random maze with guaranteed connectivity.

    Parameters
    ----------
    rows      : int — number of rows
    cols      : int — number of columns
    wall_prob : float — probability that any cell is a wall (default 0.25)
    seed      : int or None — random seed for reproducibility

    Returns
    -------
    maze : 2D list of int (0 = free, 1 = wall)
    """
    if seed is not None:
        random.seed(seed)

    start = (0, 0)
    goal  = (rows - 1, cols - 1)

    # Fill grid randomly
    maze = [[1] * cols for _ in range(rows)]
    maze[0][0]           = 0    # always free
    maze[rows-1][cols-1] = 0    # always free

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in [start, goal]:
                maze[r][c] = 1 if random.random() < wall_prob else 0

    # Fallback: carve a guaranteed L-shaped path if BFS fails
    path, _, _ = bfs(maze, start, goal)
    if path is None:
        for i in range(rows):
            maze[i][0] = 0          # left column
        for j in range(cols):
            maze[rows-1][j] = 0     # bottom row

    return maze
