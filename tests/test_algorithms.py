"""
tests/test_algorithms.py
-------------------------
Unit tests for BFS, DFS, A*, and Adaptive A*.
Run with:  pytest tests/
"""

import pytest
from src.algorithms.bfs            import bfs
from src.algorithms.dfs            import dfs
from src.algorithms.astar          import astar
from src.algorithms.adaptive_astar import adaptive_astar_dynamic

# ── Shared test mazes ─────────────────────────────────────────────────────────

SIMPLE_MAZE = [
    [0, 0, 0],
    [1, 1, 0],
    [0, 0, 0],
]

BLOCKED_MAZE = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
]

OPEN_MAZE = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

START = (0, 0)
GOAL  = (2, 2)


# ── BFS Tests ─────────────────────────────────────────────────────────────────

class TestBFS:
    def test_finds_path_simple_maze(self):
        path, explored, _ = bfs(SIMPLE_MAZE, START, GOAL)
        assert path is not None
        assert path[0] == START
        assert path[-1] == GOAL

    def test_returns_none_when_blocked(self):
        path, _, _ = bfs(BLOCKED_MAZE, START, GOAL)
        assert path is None

    def test_path_is_optimal(self):
        path, _, _ = bfs(OPEN_MAZE, (0, 0), (4, 4))
        # BFS guarantees shortest path; Manhattan lower bound = 8
        assert path is not None
        assert len(path) - 1 == 8

    def test_invalid_start(self):
        path, _, _ = bfs(SIMPLE_MAZE, (0, 1), (2, 2))
        # (0,1) is free in SIMPLE_MAZE, but let's test wall start
        wall_maze = [[1, 0], [0, 0]]
        path, _, _ = bfs(wall_maze, (0, 0), (1, 1))
        assert path is None


# ── DFS Tests ─────────────────────────────────────────────────────────────────

class TestDFS:
    def test_finds_path_simple_maze(self):
        path, explored, _ = dfs(SIMPLE_MAZE, START, GOAL)
        assert path is not None
        assert path[0] == START
        assert path[-1] == GOAL

    def test_returns_none_when_blocked(self):
        path, _, _ = dfs(BLOCKED_MAZE, START, GOAL)
        assert path is None

    def test_path_not_necessarily_optimal(self):
        # DFS finds A path but not necessarily the shortest
        path, _, _ = dfs(OPEN_MAZE, (0, 0), (4, 4))
        assert path is not None
        assert len(path) - 1 >= 8   # may be longer than optimal


# ── A* Tests ──────────────────────────────────────────────────────────────────

class TestAStar:
    def test_finds_path_simple_maze(self):
        path, explored, _ = astar(SIMPLE_MAZE, START, GOAL)
        assert path is not None
        assert path[0] == START
        assert path[-1] == GOAL

    def test_returns_none_when_blocked(self):
        path, _, _ = astar(BLOCKED_MAZE, START, GOAL)
        assert path is None

    def test_path_is_optimal(self):
        path, _, _ = astar(OPEN_MAZE, (0, 0), (4, 4))
        assert path is not None
        assert len(path) - 1 == 8

    def test_explores_fewer_nodes_than_bfs(self):
        _, bfs_explored, _ = bfs(OPEN_MAZE,   (0, 0), (4, 4))
        _, ast_explored, _ = astar(OPEN_MAZE, (0, 0), (4, 4))
        assert len(ast_explored) <= len(bfs_explored)


# ── Adaptive A* Tests ─────────────────────────────────────────────────────────

class TestAdaptiveAStar:
    def test_reaches_goal_simple_maze(self):
        result, frames = adaptive_astar_dynamic(
            SIMPLE_MAZE, START, GOAL,
            change_frequency=5, max_changes=1, record_frames=False
        )
        assert result["success"] is True
        assert result["path_length"] is not None
        assert result["replan_count"] >= 1

    def test_records_frames_when_requested(self):
        result, frames = adaptive_astar_dynamic(
            OPEN_MAZE, (0, 0), (4, 4),
            change_frequency=3, max_changes=1, record_frames=True
        )
        assert len(frames) > 0

    def test_returns_failure_on_blocked_maze(self):
        result, _ = adaptive_astar_dynamic(
            BLOCKED_MAZE, START, GOAL,
            change_frequency=1, max_changes=0
        )
        assert result["success"] is False
