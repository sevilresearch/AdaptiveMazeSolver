# Step-by-Step GitHub Upload Guide

## Step 1: Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `adaptive-astar-path-planning`
3. Description: `Adaptive A* Path Planning in Dynamic Environments — AIAA 2025`
4. Set to **Public**
5. Click **Create repository**

---

## Step 2: Upload via GitHub Web Interface (Easiest)
1. Open the repository you just created
2. Click **"uploading an existing file"**
3. Drag and drop ALL files maintaining the folder structure
4. Write commit message: `Initial commit: Add algorithms, experiments, and results`
5. Click **Commit changes**

---

## Step 3: Upload via Git (Command Line)
```bash
# Navigate to your project folder
cd adaptive-astar

# Initialize git
git init

# Add remote repository
git remote add origin https://github.com/sevilresearch/adaptive-astar-path-planning.git

# Stage all files
git add .

# First commit
git commit -m "Initial commit: Add algorithms, experiments, and results"

# Push to GitHub
git push -u origin main
```

---

## Step 4: Add Results After Running Experiments
```bash
# After running python run_experiments.py:
git add results/
git commit -m "results: Add figures, animations, and metrics CSV"
git push
```

---

## Recommended Commit Messages
```bash
git commit -m "feat: Add BFS, DFS, A*, Adaptive A* implementations"
git commit -m "feat: Add dynamic maze environment"
git commit -m "test: Add unit tests for all algorithms"
git commit -m "results: Add experimental results for all grid sizes"
git commit -m "docs: Add user manual and experiment setup guide"
git commit -m "fix: Fix replan count tracking in Adaptive A*"
```
