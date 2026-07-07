from __future__ import annotations

import heapq
import itertools
import time
from typing import Dict

from pathfinding.algorithms.base import PathfindingAlgorithm, SearchResult
from pathfinding.grid import Grid, Position
from pathfinding.heuristics import Heuristic, get_heuristic


class AStar(PathfindingAlgorithm):

    name = "astar"

    def __init__(self, heuristic: Heuristic | str = "manhattan"):
        self.heuristic = get_heuristic(heuristic) if isinstance(heuristic, str) else heuristic

    def solve(self, grid: Grid, start: Position, goal: Position, allow_diagonal: bool = False) -> SearchResult:
        start_time = time.perf_counter()
        counter = itertools.count()

        open_heap = [(0.0, next(counter), start)]
        g_score: Dict[Position, float] = {start: 0.0}
        came_from: Dict[Position, Position] = {}
        closed: set[Position] = set()
        visited_order: list[Position] = []

        while open_heap:
            _, _, current = heapq.heappop(open_heap)
            if current in closed:
                continue
            closed.add(current)
            visited_order.append(current)

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return SearchResult(
                    success=True,
                    path=path,
                    visited_order=visited_order,
                    nodes_expanded=len(closed),
                    path_cost=g_score[current],
                    time_seconds=time.perf_counter() - start_time,
                    algorithm_name=self.name,
                )

            for neighbor in grid.neighbors(current, allow_diagonal):
                tentative_g = g_score[current] + self.step_cost(current, neighbor)
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (f_score, next(counter), neighbor))

        return SearchResult(
            success=False,
            visited_order=visited_order,
            nodes_expanded=len(closed),
            time_seconds=time.perf_counter() - start_time,
            algorithm_name=self.name,
        )
