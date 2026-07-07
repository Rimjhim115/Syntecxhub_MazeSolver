"""
Real-time animated Pygame visualizer.

This is the "wow factor" demo -- a resizable window that plays back the
algorithm's exploration frame-by-frame (frontier lighting up, then the
final path drawn on top), rather than only showing a finished screenshot.
Kept isolated in its own module so `pip install pathfinding-sim` without
Pygame still works for the core algorithms + terminal UI.
"""
from __future__ import annotations

from pathfinding.algorithms.base import SearchResult
from pathfinding.grid import Grid, Position

COLORS = {
    "background": (30, 30, 30),
    "wall": (74, 74, 74),
    "free": (20, 20, 20),
    "visited": (59, 110, 165),
    "path": (62, 207, 142),
    "start": (230, 57, 70),
    "goal": (255, 209, 102),
    "grid_line": (45, 45, 45),
}


def run(
    grid: Grid,
    start: Position,
    goal: Position,
    result: SearchResult,
    cell_size: int = 20,
    fps: int = 60,
    steps_per_frame: int = 4,
) -> None:
    import pygame

    pygame.init()
    width_px = grid.width * cell_size
    height_px = grid.height * cell_size + 40
    screen = pygame.display.set_mode((width_px, height_px))
    pygame.display.set_caption(f"AI Pathfinding Simulator — {result.algorithm_name.upper()}")
    font = pygame.font.SysFont("consolas", 16)
    clock = pygame.time.Clock()

    def draw_cell(pos: Position, color) -> None:
        r, c = pos
        rect = (c * cell_size, r * cell_size, cell_size - 1, cell_size - 1)
        pygame.draw.rect(screen, color, rect)

    def draw_base() -> None:
        screen.fill(COLORS["background"])
        for r in range(grid.height):
            for c in range(grid.width):
                color = COLORS["wall"] if grid.cells[r][c] == 1 else COLORS["free"]
                draw_cell((r, c), color)

    revealed = 0
    visited_so_far: list = []
    running = True
    finished = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if not finished and revealed < len(result.visited_order):
            for _ in range(steps_per_frame):
                if revealed >= len(result.visited_order):
                    break
                visited_so_far.append(result.visited_order[revealed])
                revealed += 1
        elif revealed >= len(result.visited_order):
            finished = True

        draw_base()
        for pos in visited_so_far:
            draw_cell(pos, COLORS["visited"])
        if finished and result.success:
            for pos in result.path:
                draw_cell(pos, COLORS["path"])
        draw_cell(start, COLORS["start"])
        draw_cell(goal, COLORS["goal"])

        status = "exploring..." if not finished else ("solved!" if result.success else "no path found")
        label = font.render(
            f"{result.algorithm_name.upper()}  |  {status}  |  ESC to quit", True, (230, 230, 230)
        )
        screen.blit(label, (8, grid.height * cell_size + 8))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
