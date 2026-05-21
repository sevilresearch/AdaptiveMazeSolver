"""
algorithms/adaptive_astar.py
-----------------------------
Adaptive A* with event-driven replanning for dynamic maze environments.
Replans only when the current path is blocked by new obstacles.
"""

import time
from collections import deque
from src.algorithms.astar import astar
from src.environment.dynamic_maze import DynamicMaze


def adaptive_astar_dynamic(base_maze, start, goal,
                            change_frequency=3, max_changes=2,
                            size_label="", record_frames=False):
    """
    Adaptive A* that replans when obstacles appear on the current path.

    Parameters
    ----------
    base_maze        : 2D list of int  (0 = free, 1 = wall)
    start            : (row, col) tuple
    goal             : (row, col) tuple
    change_frequency : apply maze change every N steps
    max_changes      : number of cells toggled per change event
    size_label       : string label for logging (e.g. "30x30")
    record_frames    : if True, capture frames for animation

    Returns
    -------
    result : dict with keys:
        success, path_length, nodes_expanded, runtime_s,
        replan_count, avg_replan_time, memory_nodes
    frames : list of frame dicts (empty if record_frames=False)
    """
    dynamic_maze = DynamicMaze(base_maze)
    current_pos  = start
    total_path   = [start]
    total_nodes  = 0
    replan_count = 0
    replan_times = []
    step         = 0
    current_path = deque()
    frames       = []

    while current_pos != goal:

        # ── Step 1: Decide whether replanning is needed ──────────────────
        replan_needed = (len(current_path) == 0)
        if not replan_needed:
            cur_state = dynamic_maze.get_state()
            for pos in current_path:
                if cur_state[pos[0]][pos[1]] == 1:   # obstacle on planned path
                    replan_needed = True
                    break

        # ── Step 2: Replan using A* on current maze state ────────────────
        if replan_needed:
            t0 = time.perf_counter()
            new_path, explored, _ = astar(dynamic_maze.get_state(),
                                          current_pos, goal)
            replan_time   = time.perf_counter() - t0
            total_nodes  += len(explored)
            replan_count += 1
            replan_times.append(replan_time)

            if new_path is None:
                return {
                    "success":          False,
                    "path_length":      None,
                    "nodes_expanded":   total_nodes,
                    "runtime_s":        sum(replan_times),
                    "replan_count":     replan_count,
                    "avg_replan_time":  (sum(replan_times) / len(replan_times)
                                         if replan_times else 0),
                    "memory_nodes":     total_nodes,
                }, frames

            current_path = deque(new_path[1:])   # skip current position

        # ── Step 3: Capture frame for animation (before moving) ──────────
        if record_frames:
            frames.append({
                "maze":         dynamic_maze.get_state(),
                "robot":        current_pos,
                "total_path":   list(total_path),
                "planned_path": [current_pos] + list(current_path),
                "step":         step,
                "replans":      replan_count,
            })

        # ── Step 4: Move one step along planned path ──────────────────────
        next_pos    = current_path.popleft()
        current_pos = next_pos
        total_path.append(current_pos)
        step += 1

        # ── Step 5: Apply stochastic maze change every N steps ────────────
        if step % change_frequency == 0:
            dynamic_maze.apply_random_change(max_changes)

    # Final frame — robot has reached goal
    if record_frames:
        frames.append({
            "maze":         dynamic_maze.get_state(),
            "robot":        current_pos,
            "total_path":   list(total_path),
            "planned_path": [current_pos],
            "step":         step,
            "replans":      replan_count,
        })

    return {
        "success":         True,
        "path_length":     len(total_path) - 1,
        "nodes_expanded":  total_nodes,
        "runtime_s":       sum(replan_times),
        "replan_count":    replan_count,
        "avg_replan_time": (sum(replan_times) / len(replan_times)
                            if replan_times else 0),
        "memory_nodes":    total_nodes,
    }, frames
