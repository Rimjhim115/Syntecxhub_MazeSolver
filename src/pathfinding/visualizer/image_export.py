"""Render a solved maze to a PNG using Matplotlib -- used for README screenshots
and for anyone who wants a shareable static image instead of a live demo."""
from __future__ import annotations

from pathfinding.algorithms.base import SearchResult
from pathfinding.grid import Grid, Position


def save_image(
    grid: Grid,
    start: Position,
    goal: Position,
    result: SearchResult,
    output_path: str = "maze_result.png",
) -> str:
    import matplotlib.pyplot as plt
    import numpy as np

    # 0 = free, 1 = wall, 2 = visited, 3 = path, 4 = start, 5 = goal
    canvas = np.array(grid.cells, dtype=int)
    for r, c in result.visited_order:
        if canvas[r, c] == 0:
            canvas[r, c] = 2
    for r, c in result.path:
        canvas[r, c] = 3
    sr, sc = start
    gr, gc = goal
    canvas[sr, sc] = 4
    canvas[gr, gc] = 5

    colors = ["#1e1e1e", "#4a4a4a", "#3b6ea5", "#3ecf8e", "#e63946", "#ffd166"]
    cmap = plt.matplotlib.colors.ListedColormap(colors)

    fig, ax = plt.subplots(figsize=(grid.width / 4, grid.height / 4))
    ax.imshow(canvas, cmap=cmap, vmin=0, vmax=5)
    ax.set_xticks([])
    ax.set_yticks([])
    title = "SOLVED" if result.success else "NO PATH FOUND"
    ax.set_title(f"{result.algorithm_name.upper()} — {title} ({result.path_length} steps)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path
