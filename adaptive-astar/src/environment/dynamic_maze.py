"""
environment/dynamic_maze.py
----------------------------
DynamicMaze class: wraps a static maze and supports
stochastic obstacle toggling at runtime.
"""

import random


class DynamicMaze:
    """
    A maze that can change at runtime by randomly toggling cells.

    Parameters
    ----------
    base_maze : 2D list of int  (0 = free, 1 = wall)
    """

    def __init__(self, base_maze):
        # Deep copy so original maze is not modified
        self.maze = [row[:] for row in base_maze]
        self.rows, self.cols = len(self.maze), len(self.maze[0])

    def get_state(self):
        """Return a deep copy of the current maze state."""
        return [row[:] for row in self.maze]

    def apply_random_change(self, num_changes=2):
        """
        Toggle `num_changes` random cells (excluding start and goal).

        Parameters
        ----------
        num_changes : int — number of cells to toggle
        """
        # Exclude start (0,0) and goal (rows-1, cols-1)
        protected = {(0, 0), (self.rows - 1, self.cols - 1)}
        candidates = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in protected
        ]
        chosen = random.sample(candidates, min(num_changes, len(candidates)))
        for r, c in chosen:
            self.maze[r][c] = 1 - self.maze[r][c]   # toggle 0↔1
