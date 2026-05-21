"""
utils/metrics.py
-----------------
Evaluation helpers: run a solver and collect performance metrics,
then aggregate across multiple trials.
"""

import time


def run_and_evaluate(solver_func, maze, start, goal):
    """
    Run a solver once and return a metrics dict.

    Parameters
    ----------
    solver_func : callable — bfs, dfs, or astar
    maze        : 2D list of int
    start       : (row, col)
    goal        : (row, col)

    Returns
    -------
    dict with: success, path_length, nodes_expanded, runtime_s, memory_nodes
    """
    t0 = time.perf_counter()
    path, explored, came_from = solver_func(maze, start, goal)
    t1 = time.perf_counter()

    success = path is not None
    return {
        "success":        success,
        "path_length":    len(path) - 1 if success else None,
        "nodes_expanded": len(explored),
        "runtime_s":      t1 - t0,
        "memory_nodes":   len(came_from) + len(explored),
    }


def average_metrics(results):
    """
    Aggregate metrics across multiple runs of BFS / DFS / A*.

    Parameters
    ----------
    results : list of dicts from run_and_evaluate()

    Returns
    -------
    dict of averaged metrics
    """
    total      = len(results)
    successful = [r for r in results if r["success"]]
    avg_path   = (sum(r["path_length"] for r in successful) / len(successful)
                  if successful else None)
    return {
        "success_rate":       (len(successful) / total) * 100,
        "avg_path_length":    avg_path,
        "avg_nodes_expanded": sum(r["nodes_expanded"] for r in results) / total,
        "avg_runtime_s":      sum(r["runtime_s"]      for r in results) / total,
        "avg_memory_nodes":   sum(r["memory_nodes"]   for r in results) / total,
        "avg_replan_count":   0,
        "avg_replan_time":    0,
    }


def average_adaptive_metrics(results):
    """
    Aggregate metrics across multiple runs of Adaptive A*.

    Parameters
    ----------
    results : list of dicts from adaptive_astar_dynamic()

    Returns
    -------
    dict of averaged metrics
    """
    total      = len(results)
    successful = [r for r in results if r.get("success", False)]

    if total == 0:
        return {
            "success_rate": 0, "avg_path_length": None,
            "avg_nodes_expanded": 0, "avg_runtime_s": 0,
            "avg_replan_count": 0, "avg_replan_time": 0,
            "avg_memory_nodes": 0,
        }

    return {
        "success_rate":       (len(successful) / total) * 100,
        "avg_path_length":    (sum(r["path_length"] for r in successful) / len(successful)
                               if successful else None),
        "avg_nodes_expanded": sum(r["nodes_expanded"]  for r in results) / total,
        "avg_runtime_s":      sum(r["runtime_s"]       for r in results) / total,
        "avg_replan_count":   sum(r["replan_count"]    for r in results) / total,
        "avg_replan_time":    sum(r["avg_replan_time"] for r in results) / total,
        "avg_memory_nodes":   sum(r.get("memory_nodes", 0) for r in results) / total,
    }
