import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pathfinding.algorithms import AStar
from pathfinding.maze_generator import generate_perfect_maze, generate_random_maze


def test_random_maze_is_always_solvable():
    for seed in range(5):
        grid, start, goal = generate_random_maze(15, 15, obstacle_density=0.3, seed=seed)
        result = AStar().solve(grid, start, goal)
        assert result.success, f"seed {seed} produced an unsolvable maze"


def test_perfect_maze_is_always_solvable():
    for seed in range(5):
        grid, start, goal = generate_perfect_maze(15, 15, seed=seed)
        result = AStar().solve(grid, start, goal)
        assert result.success, f"seed {seed} produced an unsolvable maze"


def test_maze_dimensions_match_request():
    grid, _, _ = generate_random_maze(20, 12, seed=1)
    assert grid.width == 20
    assert grid.height == 12
