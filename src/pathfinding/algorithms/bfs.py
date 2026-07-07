from __future__ import annotations

import time
from collections import deque
from typing import Dict

from pathfinding.algorithms.base import PathfindingAlgorithm, SearchResult
from pathfinding.grid import Grid, Position


class BFS(PathfindingAlgorithm):

    name = "bfs"

    def solve(self, grid: Grid, start: Position, goal: Position, allow_diagonal: bool = False) -> SearchResult:
        start_time = time.perf_counter()
        frontier = deque([start])
        came_from: Dict[Position, Position] = {}
        visited = {start}
        visited_order = [start]

        while frontier:
            current = frontier.popleft()
            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return SearchResult(
                    success=True,
                    path=path,
                    visited_order=visited_order,
                    nodes_expanded=len(visited),
                    path_cost=len(path) - 1,
                    time_seconds=time.perf_counter() - start_time,
                    algorithm_name=self.name,
                )
            for neighbor in grid.neighbors(current, allow_diagonal):
                if neighbor not in visited:
                    visited.add(neighbor)
                    visited_order.append(neighbor)
                    came_from[neighbor] = current
                    frontier.append(neighbor)

        return SearchResult(
            success=False,
            visited_order=visited_order,
            nodes_expanded=len(visited),
            time_seconds=time.perf_counter() - start_time,
            algorithm_name=self.name,
        )
