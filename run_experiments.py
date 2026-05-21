"""
run_experiments.py
------------------
Main entry point: reproduces all experiments from the paper.

Usage
-----
    python run_experiments.py

Outputs (written to results/)
------------------------------
    results/figures/   — maze images, path plots, GIF animations, charts
    results/tables/    — Phase3_Results.csv with all averaged metrics
"""

import random
import numpy as np
import pandas as pd
import os

# Create required directories if they don't exist
os.makedirs('results/figures', exist_ok=True)
os.makedirs('results/tables', exist_ok=True)
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
from src.environment.maze            import generate_multi_path_maze
from src.algorithms.bfs              import bfs
from src.algorithms.dfs              import dfs
from src.algorithms.astar            import astar
from src.algorithms.adaptive_astar   import adaptive_astar_dynamic
from src.utils.metrics               import (run_and_evaluate,
                                             average_metrics,
                                             average_adaptive_metrics)
from src.utils.visualization         import (save_initial_maze,
                                             save_solver_path,
                                             save_animation,
                                             save_all_charts,
                                             save_replan_chart)

# ── Experiment configuration ──────────────────────────────────────────────────
RANDOM_SEED      = 42
GRID_SIZES       = [10, 15, 20, 25, 30]
MAZES_PER_SIZE   = 5     # number of mazes averaged per grid size
ADAPTIVE_TRIALS  = 3     # Adaptive A* trials per maze
ANIMATION_FPS    = 8     # frames per second for GIF output
CHANGE_FREQUENCY = 3     # apply maze change every N steps
MAX_CHANGES      = 2     # cells toggled per change event
WALL_PROB        = 0.25  # wall probability in generated mazes
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    size_order     = [f"{s}x{s}" for s in GRID_SIZES]
    global_summary = []

    print("=" * 70)
    print("  Adaptive A* Path Planning — Experiment Runner")
    print("=" * 70)

    for size in GRID_SIZES:
        start      = (0, 0)
        goal       = (size - 1, size - 1)
        size_label = f"{size}x{size}"

        print(f"\n{'─'*70}")
        print(f"  Grid: {size_label}   start={start}   goal={goal}")
        print(f"{'─'*70}")

        # Generate mazes (first maze used for demo images / animation)
        mazes     = [generate_multi_path_maze(size, size, WALL_PROB)
                     for _ in range(MAZES_PER_SIZE)]
        demo_maze = mazes[0]

        # ── Save initial maze image ────────────────────────────────────
        save_initial_maze(demo_maze, size_label)

        # ── Save static solver path images (demo maze) ─────────────────
        for algo_fn, name, color in [
            (bfs,   "BFS", "dodgerblue"),
            (dfs,   "DFS", "tomato"),
            (astar, "A*",  "limegreen"),
        ]:
            path, explored, _ = algo_fn(demo_maze, start, goal)
            save_solver_path(demo_maze, path, explored, size_label, name, color)

        # ── Save Adaptive A* animation (GIF) ──────────────────────────
        print(f"  Running Adaptive A* on demo maze for animation ...")
        anim_result, frames = adaptive_astar_dynamic(
            demo_maze, start, goal,
            change_frequency=CHANGE_FREQUENCY,
            max_changes=MAX_CHANGES,
            size_label=size_label,
            record_frames=True,
        )
        if frames:
            save_animation(frames, size, size, start, goal,
                           size_label, fps=ANIMATION_FPS)
        else:
            print(f"   No frames — robot could not reach goal on demo maze.")

        # ── Collect metrics over all mazes ─────────────────────────────
        bfs_results, dfs_results, astar_results = [], [], []
        for m in mazes:
            bfs_results.append(run_and_evaluate(bfs,   m, start, goal))
            dfs_results.append(run_and_evaluate(dfs,   m, start, goal))
            astar_results.append(run_and_evaluate(astar, m, start, goal))

        adaptive_results = []
        for maze_idx, maze in enumerate(mazes, 1):
            for trial in range(ADAPTIVE_TRIALS):
                result, _ = adaptive_astar_dynamic(
                    maze, start, goal,
                    change_frequency=CHANGE_FREQUENCY,
                    max_changes=MAX_CHANGES,
                    size_label=size_label,
                    record_frames=False,
                )
                adaptive_results.append(result)
                pl_str = str(result["path_length"]) if result["path_length"] else "—"
                status = "OK" if result["success"] else "FAIL"
                print(f"  maze {maze_idx}/trial {trial+1} [{status}]  "
                      f"steps={pl_str:>5}  "
                      f"replans={result['replan_count']:>3}  "
                      f"nodes={result['nodes_expanded']:>6}")

        # ── Average metrics ────────────────────────────────────────────
        avg_bfs      = average_metrics(bfs_results)
        avg_dfs      = average_metrics(dfs_results)
        avg_astar    = average_metrics(astar_results)
        avg_adaptive = average_adaptive_metrics(adaptive_results)

        for algo, avg in [("BFS",         avg_bfs),
                          ("DFS",         avg_dfs),
                          ("A*",          avg_astar),
                          ("Adaptive A*", avg_adaptive)]:
            global_summary.append({
                "size":               size_label,
                "algo":               algo,
                "success_rate":       round(avg["success_rate"], 2),
                "avg_path_length":    round(avg["avg_path_length"], 2)
                                      if avg["avg_path_length"] else None,
                "avg_nodes_expanded": round(avg["avg_nodes_expanded"], 2),
                "avg_runtime_s":      round(avg["avg_runtime_s"], 6),
                "avg_replan_count":   round(avg.get("avg_replan_count", 0), 2),
                "avg_replan_time":    round(avg.get("avg_replan_time", 0), 6),
                "avg_memory_nodes":   round(avg.get("avg_memory_nodes", 0), 2),
            })

        # Per-size console summary
        print(f"\n  {'Algorithm':<14} {'Success%':>9} {'AvgPath':>9} "
              f"{'AvgNodes':>10} {'AvgRT(ms)':>11} {'AvgReplans':>11}")
        print(f"  {'─'*14} {'─'*9} {'─'*9} {'─'*10} {'─'*11} {'─'*11}")
        for algo, avg in [("BFS",         avg_bfs),
                          ("DFS",         avg_dfs),
                          ("A*",          avg_astar),
                          ("Adaptive A*", avg_adaptive)]:
            pl = f"{avg['avg_path_length']:.1f}" if avg["avg_path_length"] else "N/A"
            print(f"  {algo:<14} {avg['success_rate']:>8.1f}%  {pl:>8}  "
                  f"{avg['avg_nodes_expanded']:>9.1f}  "
                  f"{avg['avg_runtime_s']*1000:>9.3f}ms  "
                  f"{avg.get('avg_replan_count', 0):>10.2f}")

    # ── Final summary ──────────────────────────────────────────────────────
    summary_df = pd.DataFrame(global_summary)
    summary_df["size"] = pd.Categorical(
        summary_df["size"], categories=size_order, ordered=True)
    summary_df = summary_df.sort_values(["size", "algo"]).reset_index(drop=True)

    print("\n" + "=" * 70)
    print("  FINAL RESULTS")
    print("=" * 70)
    print(summary_df.to_string(index=False))

    summary_df.to_csv("results/tables/results.csv", index=False)
    print("\n   → Saved: results/tables/results.csv")

    save_all_charts(summary_df)
    save_replan_chart(summary_df)

    print("\n" + "=" * 70)
    print("  Experiment complete.")
    print("  See results/figures/ for all plots and animations.")
    print("  See results/tables/results.csv for all metrics.")
    print("=" * 70)
