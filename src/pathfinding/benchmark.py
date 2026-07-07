"""
Benchmark harness: run every registered algorithm on the *same* maze and
report nodes expanded, path cost, and wall-clock time side by side.

This is the single feature that most clearly separates "I implemented
A*" from "I understand why A* is a good algorithm" -- it produces
evidence, not just a claim.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from pathfinding.algorithms import ALGORITHM_REGISTRY, get_algorithm
from pathfinding.algorithms.base import SearchResult
from pathfinding.grid import Grid, Position


@dataclass
class BenchmarkRow:
    algorithm: str
    success: bool
    path_length: int
    path_cost: float
    nodes_expanded: int
    time_ms: float


def run_benchmark(
    grid: Grid,
    start: Position,
    goal: Position,
    heuristic: str = "manhattan",
    allow_diagonal: bool = False,
) -> List[BenchmarkRow]:
    rows: List[BenchmarkRow] = []
    for name in ALGORITHM_REGISTRY:
        algo = get_algorithm(name, heuristic=heuristic)
        result: SearchResult = algo.solve(grid.copy(), start, goal, allow_diagonal=allow_diagonal)
        rows.append(
            BenchmarkRow(
                algorithm=name,
                success=result.success,
                path_length=result.path_length,
                path_cost=result.path_cost,
                nodes_expanded=result.nodes_expanded,
                time_ms=result.time_seconds * 1000,
            )
        )
    return rows


def print_table(rows: List[BenchmarkRow]) -> None:
    headers = ["Algorithm", "Solved", "Path Len", "Path Cost", "Nodes Expanded", "Time (ms)"]
    widths = [12, 8, 10, 11, 16, 10]
    line = "".join(h.ljust(w) for h, w in zip(headers, widths))
    print(line)
    print("-" * sum(widths))
    for row in rows:
        cells = [
            row.algorithm,
            "yes" if row.success else "no",
            str(row.path_length),
            f"{row.path_cost:.2f}",
            str(row.nodes_expanded),
            f"{row.time_ms:.3f}",
        ]
        print("".join(c.ljust(w) for c, w in zip(cells, widths)))


def save_chart(rows: List[BenchmarkRow], output_path: str = "benchmark.png") -> str:
    import matplotlib.pyplot as plt

    names = [r.algorithm for r in rows]
    expanded = [r.nodes_expanded for r in rows]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(names, expanded, color=["#3ecf8e", "#3b6ea5", "#e63946"])
    ax.set_ylabel("Nodes Expanded")
    ax.set_title("Search Efficiency: Nodes Expanded per Algorithm")
    for bar, value in zip(bars, expanded):
        ax.text(bar.get_x() + bar.get_width() / 2, value, str(value), ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path
