![CI](https://github.com/Rimjhim115/Syntecxhub_MazeSolver/actions/workflows/ci.yml/badge.svg)
# Maze Solver - AI PathFinding Simulation
A maze generator and solver comparing A*, BFS, and Dijkstra's algorithm, with live visualization and a built-in benchmark mode.
I have added 3 different search algorithms to see the difference between the algorithms practically.It shows how many nodes each one had to check to find the same path.

#Features
- A*, BFS, and Dijkstra, all using the same interface so I could swap between them easily
- Two maze generators — one that's always solvable by construction, one that's random and gets validated before use
- Terminal, Pygame, and static image visualization
- Unit tests + CI running on every push

#Result
Same path, but A* checked about 25% fewer nodes than the other two — that's the heuristic actually doing its job.
