import heapq
from node import Node


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(maze):

    start_node = Node(maze.start)
    goal_node = Node(maze.goal)

    open_list = []
    closed_set = set()

    heapq.heappush(open_list, start_node)

    while open_list:

        current = heapq.heappop(open_list)

        if current == goal_node:

            path = []

            while current:

                path.append(current.position)
                current = current.parent

            return path[::-1]

        closed_set.add(current.position)

        directions = [
            (-1,0),
            (1,0),
            (0,-1),
            (0,1)
        ]

        for dr, dc in directions:

            row = current.position[0] + dr
            col = current.position[1] + dc

            if not maze.is_valid(row, col):
                continue

            if (row, col) in closed_set:
                continue

            neighbor = Node((row, col), current)

            neighbor.g = current.g + 1
            neighbor.h = heuristic(neighbor.position, goal_node.position)
            neighbor.f = neighbor.g + neighbor.h

            skip = False

            for node in open_list:
                if neighbor == node and neighbor.g >= node.g:
                    skip = True
                    break

            if not skip:
                heapq.heappush(open_list, neighbor)

    return None