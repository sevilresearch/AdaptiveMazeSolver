"""
utils/visualization.py
-----------------------
All plotting and animation utilities:
  - save_initial_maze()   : static maze image
  - save_solver_path()    : BFS/DFS/A* path overlay
  - build_display()       : RGB array for animation frames
  - save_animation()      : GIF from recorded frames
  - save_all_charts()     : 6-panel comparison chart
  - save_individual_chart(): single metric bar chart
  - save_replan_chart()   : Adaptive A* replan analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.animation import FuncAnimation, PillowWriter

# ── Colour palette (RGB 0–1) ──────────────────────────────────────────────────
C_WALL    = np.array([0.20, 0.20, 0.20])   # dark grey
C_FREE    = np.array([0.95, 0.95, 0.92])   # off-white
C_VISITED = np.array([0.70, 0.88, 1.00])   # light blue  – trail
C_PLANNED = np.array([1.00, 0.80, 0.20])   # amber       – upcoming path
C_ROBOT   = np.array([0.18, 0.55, 0.96])   # vivid blue  – agent
C_GOAL    = np.array([0.93, 0.25, 0.25])   # red         – goal
C_START   = np.array([0.20, 0.78, 0.35])   # green       – start


def build_display(frame, rows, cols, start, goal):
    """Convert a frame dict into an (rows, cols, 3) RGB array."""
    maze        = frame["maze"]
    robot       = frame["robot"]
    total_path  = set(map(tuple, frame["total_path"]))
    planned_set = set(map(tuple, frame["planned_path"]))

    grid = np.zeros((rows, cols, 3))
    for r in range(rows):
        for c in range(cols):
            pos = (r, c)
            if maze[r][c] == 1:
                grid[r, c] = C_WALL
            elif pos in planned_set and pos != robot:
                grid[r, c] = C_PLANNED
            elif pos in total_path:
                grid[r, c] = C_VISITED
            else:
                grid[r, c] = C_FREE

    # Landmarks drawn last (highest visual priority)
    grid[start[0], start[1]] = C_START
    grid[goal[0],  goal[1]]  = C_GOAL
    grid[robot[0], robot[1]] = C_ROBOT
    return grid


def save_initial_maze(maze, size_label, output_dir="results/figures"):
    """Save a plain image of the generated maze."""
    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    goal  = (rows - 1, cols - 1)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(np.array(maze), cmap="binary", origin="upper", vmin=0, vmax=1)
    ax.scatter(start[1], start[0], color="lime",  s=300, marker="*",
               edgecolors="black", zorder=5, label="Start")
    ax.scatter(goal[1],  goal[0],  color="red",   s=300, marker="X",
               edgecolors="black", zorder=5, label="Goal")
    ax.set_title(f"Initial Maze — {size_label}", fontsize=13, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    ax.legend(loc="upper right", fontsize=9)
    plt.tight_layout()

    fname = f"{output_dir}/Initial_Maze_{size_label}.png"
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"   → Saved: {fname}")


def save_solver_path(maze, path, explored_set, size_label,
                     algo_name, color, output_dir="results/figures"):
    """Save path visualization for BFS, DFS, or A*."""
    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    goal  = (rows - 1, cols - 1)

    display = np.ones((rows, cols, 3))
    for r in range(rows):
        for c in range(cols):
            display[r, c] = ([0.15, 0.15, 0.15] if maze[r][c] == 1
                             else [0.95, 0.95, 0.92])
    for (r, c) in explored_set:
        if maze[r][c] == 0:
            display[r, c] = [0.80, 0.90, 1.00]

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(display, origin="upper")
    if path:
        pr, pc = zip(*path)
        ax.plot(pc, pr, color=color, linewidth=2.5, zorder=4, label="Path")
    ax.scatter(start[1], start[0], color="lime", s=300, marker="*",
               edgecolors="black", zorder=5)
    ax.scatter(goal[1],  goal[0],  color="red",  s=300, marker="X",
               edgecolors="black", zorder=5)
    exp_patch  = mpatches.Patch(color=(0.80, 0.90, 1.00), label="Explored")
    path_patch = mpatches.Patch(color=color, label="Path")
    ax.legend(handles=[exp_patch, path_patch], loc="upper right", fontsize=9)
    ax.set_title(f"{algo_name} — {size_label}\n"
                 f"Path: {len(path)-1 if path else 'N/A'} steps  |  "
                 f"Explored: {len(explored_set)} nodes",
                 fontsize=12, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout()

    fname = (f"{output_dir}/"
             f"{algo_name.replace('*','star').replace(' ','_')}_{size_label}.png")
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"   → Saved: {fname}")


def save_animation(frames, rows, cols, start, goal,
                   size_label, fps=8, output_dir="results/figures"):
    """Render recorded frames into an animated GIF."""
    print(f"   Rendering {len(frames)} frames for {size_label} ...",
          end=" ", flush=True)

    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor("#111111")
    ax.set_facecolor("#111111")
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    im    = ax.imshow(build_display(frames[0], rows, cols, start, goal),
                      origin="upper", interpolation="nearest")
    title = ax.set_title("", color="white", fontsize=12,
                          fontweight="bold", pad=8)

    legend_items = [
        mpatches.Patch(color=C_ROBOT,   label="Robot"),
        mpatches.Patch(color=C_PLANNED, label="Planned path"),
        mpatches.Patch(color=C_VISITED, label="Visited trail"),
        mpatches.Patch(color=C_GOAL,    label="Goal"),
        mpatches.Patch(color=C_START,   label="Start"),
        mpatches.Patch(color=C_WALL,    label="Wall"),
    ]
    ax.legend(handles=legend_items, loc="upper right",
              fontsize=7, framealpha=0.6,
              facecolor="#222222", labelcolor="white")

    def update(i):
        f = frames[i]
        im.set_data(build_display(f, rows, cols, start, goal))
        title.set_text(
            f"Adaptive A*  —  {size_label}\n"
            f"Step: {f['step']}   Replans: {f['replans']}"
        )
        return [im, title]

    ani   = FuncAnimation(fig, update, frames=len(frames),
                          interval=1000 // fps, blit=True)
    fname = f"{output_dir}/Animation_AdaptiveAstar_{size_label}.gif"
    ani.save(fname, writer=PillowWriter(fps=fps))
    plt.close(fig)
    print(f"saved → {fname}")
    return fname


def save_all_charts(summary_df, output_dir="results/figures"):
    """Save 6-panel overall comparison chart and individual metric charts."""
    df = summary_df.copy()
    df["avg_runtime_ms"]     = df["avg_runtime_s"]   * 1000
    df["avg_replan_time_ms"] = df["avg_replan_time"] * 1000

    metrics = [
        ("avg_nodes_expanded", "Nodes Expanded",            "Nodes"),
        ("avg_runtime_ms",     "Runtime (ms)",              "Time (ms)"),
        ("avg_path_length",    "Path Length",               "Steps"),
        ("success_rate",       "Success Rate (%)",          "Success (%)"),
        ("avg_replan_count",   "Avg Replans (Adaptive A*)", "Replans"),
        ("avg_replan_time_ms", "Avg Replan Time (ms)",      "Time (ms)"),
    ]
    palette = {"BFS": "#4C9BE8", "DFS": "#E87C4C",
               "A*": "#4CE874", "Adaptive A*": "#C84CE8"}

    fig, axes = plt.subplots(2, 3, figsize=(22, 12))
    for i, (col, title, ylabel) in enumerate(metrics):
        ax      = axes[i // 3, i % 3]
        plot_df = df[df[col].notna()]
        if plot_df.empty:
            ax.set_visible(False); continue
        sns.barplot(data=plot_df, x="size", y=col, hue="algo",
                    palette=palette, ax=ax,
                    order=summary_df["size"].cat.categories)
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_xlabel("Grid Size", fontsize=11)
        ax.grid(axis="y", alpha=0.35)
        ax.tick_params(axis="x", rotation=30)
        for container in ax.containers:
            ax.bar_label(container, fmt="%.1f", padding=3, fontsize=8)
        ax.legend(title="Algorithm", fontsize=8, title_fontsize=9)

    plt.suptitle("BFS / DFS / A* / Adaptive A* — Full Comparison",
                 fontsize=16, fontweight="bold", y=1.01)
    plt.tight_layout()
    fname = f"{output_dir}/Overall_Comparison.png"
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"   → Saved: {fname}")


def save_replan_chart(summary_df, output_dir="results/figures"):
    """Save Adaptive A* path length vs replan count comparison."""
    df = summary_df[summary_df["algo"] == "Adaptive A*"].copy()
    if df.empty:
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    x  = np.arange(len(df))
    w  = 0.35
    b1 = ax.bar(x - w/2, df["avg_path_length"],  w,
                label="Avg Path Length",  color="#4C9BE8")
    b2 = ax.bar(x + w/2, df["avg_replan_count"], w,
                label="Avg Replan Count", color="#C84CE8")
    ax.bar_label(b1, fmt="%.1f", padding=3, fontsize=9)
    ax.bar_label(b2, fmt="%.1f", padding=3, fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(df["size"])
    ax.set_xlabel("Grid Size", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title("Adaptive A*: Path Length vs Replan Count",
                 fontsize=13, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(axis="y", alpha=0.35)
    plt.tight_layout()

    fname = f"{output_dir}/Replan_vs_PathLength.png"
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"   → Saved: {fname}")
