"""Terminal renderer: colored ASCII maze + optional step-by-step animation."""
from __future__ import annotations

import shutil
import sys
import time

from pathfinding.algorithms.base import SearchResult
from pathfinding.grid import Grid, Position

RESET = "\033[0m"
COLORS = {
    "wall": "\033[100m  \033[0m",
    "free": "\033[40m  \033[0m",
    "visited": "\033[44m  \033[0m",
    "path": "\033[42m  \033[0m",
    "start": "\033[41m  \033[0m",
    "goal": "\033[43m  \033[0m",
}


def _render(grid: Grid, start: Position, goal: Position, visited: set, path: set) -> str:
    lines = []
    for r in range(grid.height):
        row_chars = []
        for c in range(grid.width):
            pos = (r, c)
            if pos == start:
                cell = COLORS["start"]
            elif pos == goal:
                cell = COLORS["goal"]
            elif pos in path:
                cell = COLORS["path"]
            elif pos in visited:
                cell = COLORS["visited"]
            elif grid.cells[r][c] == 1:
                cell = COLORS["wall"]
            else:
                cell = COLORS["free"]
            row_chars.append(cell)
        lines.append("".join(row_chars))
    return "\n".join(lines)


def print_static(grid: Grid, start: Position, goal: Position, result: SearchResult) -> None:
    """Print the final solved maze once, no animation."""
    visited = set(result.visited_order)
    path = set(result.path)
    print(_render(grid, start, goal, visited, path))
    _print_legend()
    _print_stats(result)


def animate(grid: Grid, start: Position, goal: Position, result: SearchResult, fps: float = 30.0) -> None:
    """Redraw the maze frame-by-frame as the algorithm explores, then show the path."""
    delay = 1.0 / fps
    visited: set = set()
    term_height = grid.height + 4

    for pos in result.visited_order:
        visited.add(pos)
        sys.stdout.write(f"\033[{term_height}A")  # move cursor up to redraw in place
        print(_render(grid, start, goal, visited, set()))
        _print_legend()
        time.sleep(delay)

    if result.success:
        sys.stdout.write(f"\033[{term_height}A")
        print(_render(grid, start, goal, visited, set(result.path)))
        _print_legend()
    _print_stats(result)


def _print_legend() -> None:
    print(
        f"{COLORS['start']} Start   {COLORS['goal']} Goal   "
        f"{COLORS['visited']} Explored   {COLORS['path']} Path   {COLORS['wall']} Wall"
    )


def _print_stats(result: SearchResult) -> None:
    status = "SOLVED" if result.success else "NO PATH FOUND"
    width = shutil.get_terminal_size((80, 20)).columns
    print("-" * min(width, 60))
    print(f"Algorithm:      {result.algorithm_name}")
    print(f"Status:         {status}")
    print(f"Path length:    {result.path_length}")
    print(f"Path cost:      {result.path_cost:.2f}")
    print(f"Nodes expanded: {result.nodes_expanded}")
    print(f"Time taken:     {result.time_seconds * 1000:.2f} ms")
    print("-" * min(width, 60))
