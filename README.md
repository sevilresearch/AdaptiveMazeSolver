# Adaptive A* Path Planning in Dynamic Environments

> **Empirical Validation of Event-Driven Replanning for Real-Time Robotics**  
> Ranjitha Shivaprasad Ballakuraya · Hakki Erhan Sevil  
> University of West Florida, FL 32514  
> AIAA Conference Paper, 2025

---

## Overview

This repository contains the **complete implementation, experiments, and results** for the paper:

> *"Adaptive A* Path Planning in Dynamic Environments: Empirical Validation of  
> Event-Driven Replanning for Real-Time Robotics"*

We evaluate four path planning algorithms across static and dynamic maze environments
with grid sizes from 10×10 to 30×30, providing a reproducible benchmarking framework.

---

## Algorithms Implemented

| Algorithm | Type | Optimal | Handles Dynamics |
|-----------|------|---------|-----------------|
| BFS | Uninformed | ✅ Yes | ❌ No |
| DFS | Uninformed | ❌ No | ❌ No |
| A* | Heuristic-guided | ✅ Yes | ❌ No |
| Adaptive A* | Event-driven replanning | ~3.72% overhead | ✅ Yes |

---

## Key Results (30×30 Grid)

| Algorithm | Nodes Explored | Runtime | Path Quality | Success (Dynamic) |
|-----------|---------------|---------|--------------|-------------------|
| BFS | 666.4 | 4.53 ms | Optimal | N/A |
| DFS | 220.6 | 1.51 ms | +148% suboptimal | N/A |
| A* | 314.2 (−53% vs BFS) | 3.25 ms | Optimal | N/A |
| Adaptive A* | 637.5 (cumulative) | 3.18 ms | +3.72% mean | 73–93% |

---

## Repository Structure

```
adaptive-astar/
│
├── run_experiments.py          ← Main entry point: runs all experiments
├── requirements.txt            ← Python dependencies
│
├── src/
│   ├── algorithms/
│   │   ├── bfs.py              ← Breadth-First Search
│   │   ├── dfs.py              ← Depth-First Search
│   │   ├── astar.py            ← A* with Manhattan heuristic
│   │   └── adaptive_astar.py   ← Adaptive A* with event-driven replanning
│   │
│   ├── environment/
│   │   ├── maze.py             ← Random maze generator
│   │   └── dynamic_maze.py     ← Dynamic maze with obstacle toggling
│   │
│   └── utils/
│       ├── helpers.py          ← Shared: is_valid, get_neighbors, manhattan
│       ├── metrics.py          ← Evaluation and averaging helpers
│       └── visualization.py    ← All plotting, animation, chart saving
│
├── tests/
│   └── test_algorithms.py      ← Unit tests (pytest)
│
├── data/
│   ├── raw/                    ← Raw per-trial results
│   └── processed/              ← Aggregated CSVs used in paper
│
├── results/
│   ├── figures/                ← Maze images, path plots, GIF animations
│   └── tables/                 ← results.csv — all averaged metrics
│
├── notebooks/
│   ├── 01_algorithm_demo.ipynb ← Interactive demo of all algorithms
│   └── 02_results_analysis.ipynb ← Reproduce paper figures
│
└── docs/
    ├── user_manual.md          ← How to use the code
    └── experiment_setup.md     ← Full experimental configuration
```

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/sevilresearch/AdaptiveMazeSolver.git
cd AdaptiveMazeSolver
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run All Experiments
```bash
python run_experiments.py
```

This will:
- Generate random mazes (10×10 to 30×30)
- Run BFS, DFS, A*, and Adaptive A* on each
- Save path images and GIF animations to `results/figures/`
- Save all metrics to `results/tables/results.csv`
- Save comparison charts to `results/figures/`

### 4. Run Unit Tests
```bash
pytest tests/ -v
```

---

## Using Individual Algorithms

```python
from src.environment.maze          import generate_multi_path_maze
from src.algorithms.bfs            import bfs
from src.algorithms.astar          import astar
from src.algorithms.adaptive_astar import adaptive_astar_dynamic

# Generate a 20x20 maze
maze  = generate_multi_path_maze(20, 20, wall_prob=0.25)
start = (0, 0)
goal  = (19, 19)

# Run BFS
path, explored, _ = bfs(maze, start, goal)
print(f"BFS  — path: {len(path)-1} steps, explored: {len(explored)} nodes")

# Run A*
path, explored, _ = astar(maze, start, goal)
print(f"A*   — path: {len(path)-1} steps, explored: {len(explored)} nodes")

# Run Adaptive A* on a dynamic maze
result, frames = adaptive_astar_dynamic(
    maze, start, goal,
    change_frequency=3,   # apply change every 3 steps
    max_changes=2,        # toggle 2 cells per change
    record_frames=True    # capture frames for animation
)
print(f"Adaptive A* — success: {result['success']}, "
      f"replans: {result['replan_count']}, "
      f"path: {result['path_length']} steps")
```

---

## Reproducing Specific Paper Figures

```bash
# Static maze comparison (Figure 3 in paper)
python -c "
from src.environment.maze import generate_multi_path_maze
from src.algorithms.bfs   import bfs
from src.algorithms.astar import astar
from src.utils.visualization import save_solver_path

maze = generate_multi_path_maze(30, 30)
for fn, name, color in [(bfs,'BFS','dodgerblue'),(astar,'A*','limegreen')]:
    path, exp, _ = fn(maze, (0,0), (29,29))
    save_solver_path(maze, path, exp, '30x30', name, color)
"

# Adaptive A* animation (Figure 5 in paper)
python -c "
from src.environment.maze          import generate_multi_path_maze
from src.algorithms.adaptive_astar import adaptive_astar_dynamic
from src.utils.visualization       import save_animation

maze = generate_multi_path_maze(20, 20)
result, frames = adaptive_astar_dynamic(maze,(0,0),(19,19),record_frames=True)
save_animation(frames, 20, 20, (0,0), (19,19), '20x20')
"
```

---

## Experimental Configuration

| Parameter | Value |
|-----------|-------|
| Grid sizes | 10×10, 15×15, 20×20, 25×25, 30×30 |
| Mazes per size | 5 |
| Adaptive A* trials per maze | 3 |
| Wall probability | 0.25 |
| Change frequency | every 3 steps |
| Max cells toggled per change | 2 |
| Random seed | 42 |

---

## Citation

If you use this code in your research, please cite:

```bibtex
@inproceedings{ballakuraya2025adaptive,
  title     = {Adaptive {A*} Path Planning in Dynamic Environments:
               Empirical Validation of Event-Driven Replanning
               for Real-Time Robotics},
  author    = {Ballakuraya, Ranjitha Shivaprasad and Sevil, Hakki Erhan},
  booktitle = {AIAA SciTech Forum},
  year      = {2025},
  institution = {University of West Florida},
  url       = {https://github.com/sevilresearch/adaptive-astar}
}
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Contact

- **Ranjitha Shivaprasad Ballakuraya** — PhD Student, Dept. of Intelligent Systems & Robotics, UWF
- **Hakki Erhan Sevil** — Associate Professor, Dept. of Intelligent Systems & Robotics, UWF  
- **Research Group**: [github.com/sevilresearch](https://github.com/sevilresearch)
