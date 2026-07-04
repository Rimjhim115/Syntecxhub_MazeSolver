from maze import Maze
from astar import astar
from maze_generator import generate_maze

rows = int(input("Enter rows: "))
cols = int(input("Enter columns: "))
density = float(input("Enter obstacle density (0-1): "))

generated = generate_maze(rows, cols, density)

maze = Maze(generated)

print("\nGenerated Maze\n")
maze.print_maze()

path = astar(maze)

if path:

    for row, col in path:

        if maze.grid[row][col] not in ('S', 'G'):
            maze.grid[row][col] = '*'

    print("\nSolved Maze\n")
    maze.print_maze()

    print("\nShortest Path Length:", len(path) - 1)

else:
    print("No path found.")