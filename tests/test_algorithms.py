import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from pathfinding.algorithms import BFS, AStar, Dijkstra
from pathfinding.grid import Grid


def make_open_grid(size=5):
    return Grid(width=size, height=size)


def make_blocked_grid():
    # A fully sealed 3x3 grid: no path from (0,0) to (2,2)
    grid = Grid(width=3, height=3)
    grid.set_wall((0, 1))
    grid.set_wall((1, 0))
    grid.set_wall((1, 1))
    grid.set_wall((1, 2))
    grid.set_wall((2, 1))
    return grid


@pytest.mark.parametrize("algo_cls", [AStar, BFS, Dijkstra])
def test_finds_optimal_path_on_open_grid(algo_cls):
    grid = make_open_grid(5)
    algo = algo_cls() if algo_cls is not AStar else AStar(heuristic="manhattan")
    result = algo.solve(grid, (0, 0), (4, 4))
    assert result.success
    assert result.path[0] == (0, 0)
    assert result.path[-1] == (4, 4)
    assert result.path_length == 9  # Manhattan distance + 1 on an open grid


@pytest.mark.parametrize("algo_cls", [AStar, BFS, Dijkstra])
def test_reports_failure_when_no_path_exists(algo_cls):
    grid = make_blocked_grid()
    algo = algo_cls() if algo_cls is not AStar else AStar(heuristic="manhattan")
    result = algo.solve(grid, (0, 0), (2, 2))
    assert not result.success
    assert result.path == []


def test_astar_and_bfs_agree_on_path_length():
    grid = make_open_grid(7)
    a_result = AStar(heuristic="manhattan").solve(grid, (0, 0), (6, 6))
    b_result = BFS().solve(grid, (0, 0), (6, 6))
    assert a_result.path_length == b_result.path_length


def test_astar_expands_fewer_or_equal_nodes_than_dijkstra():
    grid = make_open_grid(9)
    a_result = AStar(heuristic="manhattan").solve(grid, (0, 0), (8, 8))
    d_result = Dijkstra().solve(grid, (0, 0), (8, 8))
    assert a_result.nodes_expanded <= d_result.nodes_expanded
