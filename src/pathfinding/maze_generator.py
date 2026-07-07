
from __future__ import annotations

import random
from collections import deque
from typing import Optional, Tuple

from pathfinding.grid import FREE, WALL, Grid, Position


def _is_reachable(grid: Grid, start: Position, goal: Position) -> bool:
    if not grid.is_walkable(start) or not grid.is_walkable(goal):
        return False
    frontier = deque([start])
    visited = {start}
    while frontier:
        current = frontier.popleft()
        if current == goal:
            return True
        for neighbor in grid.neighbors(current, allow_diagonal=False):
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)
    return False


def generate_random_maze(
    width: int,
    height: int,
    obstacle_density: float = 0.28,
    start: Optional[Position] = None,
    goal: Optional[Position] = None,
    seed: Optional[int] = None,
    max_attempts: int = 50,
) -> Tuple[Grid, Position, Position]:
    rng = random.Random(seed)
    start = start or (0, 0)
    goal = goal or (height - 1, width - 1)

    for _ in range(max_attempts):
        cells = [
            [WALL if rng.random() < obstacle_density else FREE for _ in range(width)]
            for _ in range(height)
        ]
        grid = Grid.from_matrix(cells)
        grid.set_free(start)
        grid.set_free(goal)
        if _is_reachable(grid, start, goal):
            return grid, start, goal

    raise RuntimeError(
        f"Could not generate a solvable maze in {max_attempts} attempts; "
        "try a lower obstacle_density."
    )


def generate_perfect_maze(
    width: int,
    height: int,
    start: Optional[Position] = None,
    goal: Optional[Position] = None,
    seed: Optional[int] = None,
) -> Tuple[Grid, Position, Position]:
  
    rng = random.Random(seed)
    # Carve on a grid where walls sit between cells, then map back.
    grid = Grid(width=width, height=height, cells=[[WALL] * width for _ in range(height)])

    def carve(r: int, c: int) -> None:
        grid.set_free((r, c))
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        rng.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and grid.cells[nr][nc] == WALL:
                grid.set_free((r + dr // 2, c + dc // 2))
                carve(nr, nc)

    carve(0, 0)

    start = start or (0, 0)
    goal = goal or (height - 1, width - 1)
    grid.set_free(start)
    grid.set_free(goal)

    # Guarantee the requested goal is reachable even if it lands on an
    # unlucky odd/even parity cell relative to the carve.
    if not _is_reachable(grid, start, goal):
        _carve_shortest_gap(grid, start, goal)

    return grid, start, goal


def _carve_shortest_gap(grid: Grid, start: Position, goal: Position) -> None:
    frontier = deque([start])
    came_from: dict = {}
    visited = {start}
    while frontier:
        current = frontier.popleft()
        if current == goal:
            break
        r, c = current
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if grid.in_bounds((nr, nc)) and (nr, nc) not in visited:
                visited.add((nr, nc))
                came_from[(nr, nc)] = current
                frontier.append((nr, nc))
    node = goal
    while node in came_from:
        grid.set_free(node)
        node = came_from[node]
    grid.set_free(start)
