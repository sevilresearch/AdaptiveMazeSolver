cd C:\Users\sbran\Downloads\AdaptiveMazeSolver

# Create setup.py
@"
from setuptools import setup, find_packages

setup(
    name="adaptive-astar",
    version="1.0.0",
    description="Adaptive A* Path Planning in Dynamic Environments",
    author="Ranjitha Shivaprasad Ballakuraya, Hakki Erhan Sevil",
    author_email="rballakuraya@uwf.edu, hsevil@uwf.edu",
    url="https://github.com/sevilresearch/AdaptiveMazeSolver",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "matplotlib",
        "pytest",
    ],
)
"@ | Out-File -Encoding UTF8 setup.py

# Verify it was created
dir setup.py
