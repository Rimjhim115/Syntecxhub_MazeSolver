
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from pathfinding.grid import Grid, Position


@dataclass
class SearchResult:
    """Everything a caller (CLI, GUI, benchmark) might need after a search."""

    success: bool
    path: List[Position] = field(default_factory=list)
    visited_order: List[Position] = field(default_factory=list)
    nodes_expanded: int = 0
    path_cost: float = 0.0
    time_seconds: float = 0.0
    algorithm_name: str = ""

    @property
    def path_length(self) -> int:
        return len(self.path)


class PathfindingAlgorithm(ABC):
   

    name: str = "abstract"

    @abstractmethod
    def solve(
        self,
        grid: Grid,
        start: Position,
        goal: Position,
        allow_diagonal: bool = False,
    ) -> SearchResult:
        ...

    @staticmethod
    def reconstruct_path(came_from: dict, current: Position) -> List[Position]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    @staticmethod
    def step_cost(a: Position, b: Position) -> float:
        return 1.4142135623730951 if a[0] != b[0] and a[1] != b[1] else 1.0
