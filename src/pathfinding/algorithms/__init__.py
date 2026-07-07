from pathfinding.algorithms.astar import AStar
from pathfinding.algorithms.bfs import BFS
from pathfinding.algorithms.dijkstra import Dijkstra
from pathfinding.algorithms.base import PathfindingAlgorithm, SearchResult

ALGORITHM_REGISTRY = {
    "astar": AStar,
    "bfs": BFS,
    "dijkstra": Dijkstra,
}


def get_algorithm(name: str, **kwargs) -> PathfindingAlgorithm:
    try:
        cls = ALGORITHM_REGISTRY[name.lower()]
    except KeyError as exc:
        valid = ", ".join(ALGORITHM_REGISTRY)
        raise ValueError(f"Unknown algorithm '{name}'. Valid options: {valid}") from exc
    if cls is AStar:
        return cls(heuristic=kwargs.get("heuristic", "manhattan"))
    return cls()


__all__ = ["AStar", "BFS", "Dijkstra", "PathfindingAlgorithm", "SearchResult", "get_algorithm", "ALGORITHM_REGISTRY"]
