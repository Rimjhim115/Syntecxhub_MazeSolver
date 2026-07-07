import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pathfinding.grid import Grid


def test_neighbors_orthogonal_only():
    grid = Grid(width=3, height=3)
    neighbors = set(grid.neighbors((1, 1), allow_diagonal=False))
    assert neighbors == {(0, 1), (2, 1), (1, 0), (1, 2)}


def test_neighbors_respects_walls():
    grid = Grid(width=3, height=3)
    grid.set_wall((0, 1))
    neighbors = set(grid.neighbors((1, 1), allow_diagonal=False))
    assert (0, 1) not in neighbors


def test_diagonal_corner_cutting_blocked():
    grid = Grid(width=3, height=3)
    grid.set_wall((0, 1))
    grid.set_wall((1, 0))
    neighbors = set(grid.neighbors((1, 1), allow_diagonal=True))
    assert (0, 0) not in neighbors  # both orthogonal sides blocked


def test_out_of_bounds():
    grid = Grid(width=2, height=2)
    assert not grid.in_bounds((-1, 0))
    assert not grid.in_bounds((2, 0))
