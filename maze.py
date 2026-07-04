class Maze:

    def __init__(self, source):

        if isinstance(source, str):

            with open(source, "r") as file:
                self.grid = [list(line.strip()) for line in file]

        else:
            self.grid = source

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.start = None
        self.goal = None

        for i in range(self.rows):
            for j in range(self.cols):

                if self.grid[i][j] == 'S':
                    self.start = (i, j)

                elif self.grid[i][j] == 'G':
                    self.goal = (i, j)

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.start = None
        self.goal = None

        for i in range(self.rows):
            for j in range(self.cols):

                if self.grid[i][j] == 'S':
                    self.start = (i, j)

                elif self.grid[i][j] == 'G':
                    self.goal = (i, j)

    def is_valid(self, row, col):

        return (
            0 <= row < self.rows and
            0 <= col < self.cols and
            self.grid[row][col] != '#'
        )

    def print_maze(self):

        for row in self.grid:
            print("".join(row))