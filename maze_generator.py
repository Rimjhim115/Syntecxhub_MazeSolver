import random
from maze import Maze
from astar import astar


def generate_maze(rows, cols, obstacle_density=0.3):
    while True:
        maze = []
        for i in range(rows):
            row = []
            for j in range(cols):
                if random.random() < obstacle_density:
                    row.append('#')
                else:
                    row.append('.')
            maze.append(row)
        maze[0][0] = 'S'
        maze[rows - 1][cols - 1] = 'G'
        temp = Maze(maze)
        path = astar(temp)
        if path is not None:
            return maze
def save_maze(maze, filename):
    with open(filename, "w") as file:
        for row in maze:
            file.write("".join(row) + "\n")