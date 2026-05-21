# User Manual

## Table of Contents
1. [Installation](#installation)
2. [Running Experiments](#running-experiments)
3. [Using Individual Algorithms](#using-individual-algorithms)
4. [Generating Mazes](#generating-mazes)
5. [Visualizing Results](#visualizing-results)
6. [Understanding the Output Files](#understanding-the-output-files)
7. [Troubleshooting](#troubleshooting)

---

## 1. Installation

### Requirements
- Python 3.8 or higher
- pip

### Steps
```bash
# Clone the repository
git clone https://github.com/sevilresearch/adaptive-astar.git
cd adaptive-astar

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Running Experiments

### Run all experiments (reproduces all paper results)
```bash
python run_experiments.py
```

### What it does step by step:
1. Sets random seed (42) for reproducibility
2. For each grid size (10, 15, 20, 25, 30):
   - Generates 5 random mazes
   - Runs BFS, DFS, A* on each maze
   - Runs Adaptive A* for 3 trials per maze
   - Saves path images and one GIF animation
   - Prints a metrics table to console
3. Saves `results/tables/results.csv`
4. Saves all comparison charts to `results/figures/`

### Run unit tests
```bash
pytest tests/ -v
```

---

## 3. Using Individual Algorithms

### BFS
```python
from src.algorithms.bfs import bfs

path, explored, came_from = bfs(maze, start, goal)
# path     → list of (row,col) tuples, or None if no path exists
# explored → set of all visited positions
# came_from→ dict {position: parent_position}
```

### DFS
```python
from src.algorithms.dfs import dfs

path, explored, came_from = dfs(maze, start, goal)
```

### A*
```python
from src.algorithms.astar import astar

path, explored, came_from = astar(maze, start, goal)
```

### Adaptive A*
```python
from src.algorithms.adaptive_astar import adaptive_astar_dynamic

result, frames = adaptive_astar_dynamic(
    base_maze        = maze,
    start            = (0, 0),
    goal             = (19, 19),
    change_frequency = 3,      # apply change every N steps
    max_changes      = 2,      # cells toggled per change
    record_frames    = True    # set False to skip animation data
)

# result dict keys:
# success, path_length, nodes_expanded, runtime_s,
# replan_count, avg_replan_time, memory_nodes
```

---

## 4. Generating Mazes

```python
from src.environment.maze import generate_multi_path_maze

# Basic usage
maze = generate_multi_path_maze(rows=20, cols=20)

# With custom wall density
maze = generate_multi_path_maze(20, 20, wall_prob=0.30)

# With fixed seed for reproducibility
maze = generate_multi_path_maze(20, 20, seed=42)

# maze is a 2D list: 0 = free cell, 1 = wall
# start is always (0, 0), goal is always (rows-1, cols-1)
```

---

## 5. Visualizing Results

```python
from src.utils.visualization import (
    save_initial_maze,
    save_solver_path,
    save_animation
)

# Save maze image
save_initial_maze(maze, size_label="20x20")

# Save path visualization
save_solver_path(maze, path, explored,
                 size_label="20x20",
                 algo_name="A*",
                 color="limegreen")

# Save animation GIF
save_animation(frames, rows=20, cols=20,
               start=(0,0), goal=(19,19),
               size_label="20x20", fps=8)
```

---

## 6. Understanding the Output Files

| File | Description |
|------|-------------|
| `results/figures/Initial_Maze_<size>.png` | Generated maze (walls + start/goal) |
| `results/figures/BFS_<size>.png` | BFS explored nodes + path |
| `results/figures/DFS_<size>.png` | DFS explored nodes + path |
| `results/figures/Astar_<size>.png` | A* explored nodes + path |
| `results/figures/Animation_AdaptiveAstar_<size>.gif` | Adaptive A* step-by-step GIF |
| `results/figures/Overall_Comparison.png` | 6-panel metric comparison chart |
| `results/figures/Replan_vs_PathLength.png` | Replan analysis chart |
| `results/tables/results.csv` | All averaged metrics (all algorithms, all sizes) |

### results.csv columns:
| Column | Description |
|--------|-------------|
| size | Grid size label (e.g. "30x30") |
| algo | Algorithm name |
| success_rate | % of trials that reached the goal |
| avg_path_length | Average number of steps in found path |
| avg_nodes_expanded | Average nodes explored per run |
| avg_runtime_s | Average wall-clock time in seconds |
| avg_replan_count | Average replanning events (Adaptive A* only) |
| avg_replan_time | Average time per replan in seconds |
| avg_memory_nodes | Average memory usage (node count) |

---

## 7. Troubleshooting

**Q: `ModuleNotFoundError: No module named 'src'`**  
A: Run scripts from the repository root directory:
```bash
cd adaptive-astar
python run_experiments.py
```

**Q: Animation GIF is very large**  
A: Reduce FPS or grid size in `run_experiments.py`:
```python
ANIMATION_FPS = 4   # lower FPS → smaller file
```

**Q: Experiment takes too long**  
A: Reduce the number of mazes and trials:
```python
MAZES_PER_SIZE  = 3
ADAPTIVE_TRIALS = 1
```

**Q: Results differ from the paper**  
A: Make sure `RANDOM_SEED = 42` is set and you are using the same
grid sizes and wall probability as in the paper (wall_prob=0.25).
