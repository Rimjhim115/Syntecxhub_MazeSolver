"""
Admissible heuristics for grid search.

Each function has signature (a, b) -> float and estimates the cost from
position a to position b. Keeping these as free functions (rather than
methods) makes it trivial to plug a new one into A* without touching the
algorithm itself -- see `get_heuristic`.
"""
from __future__ import annotations

import math
from typing import Callable, Tuple

Position = Tuple[int, int]
Heuristic = Callable[[Position, Position], float]


def manhattan(a: Position, b: Position) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a: Position, b: Position) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def chebyshev(a: Position, b: Position) -> float:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def octile(a: Position, b: Position) -> float:
    dr, dc = abs(a[0] - b[0]), abs(a[1] - b[1])
    return (dr + dc) + (math.sqrt(2) - 2) * min(dr, dc)


def zero(a: Position, b: Position) -> float:
    """A heuristic of 0 turns A* into Dijkstra's algorithm."""
    return 0.0


_REGISTRY: dict[str, Heuristic] = {
    "manhattan": manhattan,
    "euclidean": euclidean,
    "chebyshev": chebyshev,
    "octile": octile,
    "zero": zero,
}


def get_heuristic(name: str) -> Heuristic:
    try:
        return _REGISTRY[name.lower()]
    except KeyError as exc:
        valid = ", ".join(_REGISTRY)
        raise ValueError(f"Unknown heuristic '{name}'. Valid options: {valid}") from exc


def available_heuristics() -> list:
    return list(_REGISTRY)
