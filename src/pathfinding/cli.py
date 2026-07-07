
from __future__ import annotations

import argparse
import sys

from pathfinding.algorithms import get_algorithm
from pathfinding.heuristics import available_heuristics
from pathfinding.maze_generator import generate_perfect_maze, generate_random_maze


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pathfinder",
        description="AI Pathfinding Simulator — classical search algorithms on generated mazes.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common_maze_args(p: argparse.ArgumentParser) -> None:
        p.add_argument("--width", type=int, default=31, help="Maze width in cells")
        p.add_argument("--height", type=int, default=21, help="Maze height in cells")
        p.add_argument("--maze-type", choices=["random", "perfect"], default="perfect")
        p.add_argument("--density", type=float, default=0.28, help="Obstacle density (random maze only)")
        p.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
        p.add_argument("--diagonal", action="store_true", help="Allow 8-direction movement")

    solve_p = sub.add_parser("solve", help="Generate a maze and solve it")
    add_common_maze_args(solve_p)
    solve_p.add_argument("--algorithm", choices=["astar", "bfs", "dijkstra"], default="astar")
    solve_p.add_argument("--heuristic", choices=available_heuristics(), default="manhattan")
    solve_p.add_argument(
        "--visualize", choices=["terminal", "terminal-static", "pygame", "image"], default="terminal"
    )
    solve_p.add_argument("--fps", type=float, default=30.0, help="Terminal animation speed")
    solve_p.add_argument("--output", default="maze_result.png", help="Output path for --visualize image")

    bench_p = sub.add_parser("benchmark", help="Compare A*, BFS, and Dijkstra on the same maze")
    add_common_maze_args(bench_p)
    bench_p.add_argument("--heuristic", choices=available_heuristics(), default="manhattan")
    bench_p.add_argument("--chart", action="store_true", help="Also save a bar chart PNG")
    bench_p.add_argument("--output", default="benchmark.png")

    return parser


def _build_maze(args: argparse.Namespace):
    if args.maze_type == "perfect":
        return generate_perfect_maze(args.width, args.height, seed=args.seed)
    return generate_random_maze(args.width, args.height, args.density, seed=args.seed)


def cmd_solve(args: argparse.Namespace) -> int:
    grid, start, goal = _build_maze(args)
    algo = get_algorithm(args.algorithm, heuristic=args.heuristic)
    result = algo.solve(grid, start, goal, allow_diagonal=args.diagonal)

    if args.visualize == "terminal":
        from pathfinding.visualizer import terminal_viz
        terminal_viz.animate(grid, start, goal, result, fps=args.fps)
    elif args.visualize == "terminal-static":
        from pathfinding.visualizer import terminal_viz
        terminal_viz.print_static(grid, start, goal, result)
    elif args.visualize == "pygame":
        from pathfinding.visualizer import pygame_viz
        pygame_viz.run(grid, start, goal, result)
    elif args.visualize == "image":
        from pathfinding.visualizer import image_export
        path = image_export.save_image(grid, start, goal, result, args.output)
        print(f"Saved to {path}")

    return 0 if result.success else 1


def cmd_benchmark(args: argparse.Namespace) -> int:
    from pathfinding.benchmark import print_table, run_benchmark, save_chart

    grid, start, goal = _build_maze(args)
    rows = run_benchmark(grid, start, goal, heuristic=args.heuristic, allow_diagonal=args.diagonal)
    print_table(rows)
    if args.chart:
        path = save_chart(rows, args.output)
        print(f"\nChart saved to {path}")
    return 0


def main(argv: list | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "solve":
        return cmd_solve(args)
    if args.command == "benchmark":
        return cmd_benchmark(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
