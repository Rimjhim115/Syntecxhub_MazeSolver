
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Tuple

Position = Tuple[int, int]

WALL = 1
FREE = 0


@dataclass
class Grid:
    width: int
    height: int
    cells: list = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.cells:
            self.cells = [[FREE] * self.width for _ in range(self.height)]

    @classmethod
    def from_matrix(cls, matrix: list) -> "Grid":
        height = len(matrix)
        width = len(matrix[0]) if height else 0
        return cls(width=width, height=height, cells=[row[:] for row in matrix])

    def in_bounds(self, pos: Position) -> bool:
        r, c = pos
        return 0 <= r < self.height and 0 <= c < self.width

    def is_walkable(self, pos: Position) -> bool:
        r, c = pos
        return self.in_bounds(pos) and self.cells[r][c] == FREE

    def set_wall(self, pos: Position) -> None:
        r, c = pos
        self.cells[r][c] = WALL

    def set_free(self, pos: Position) -> None:
        r, c = pos
        self.cells[r][c] = FREE

    def neighbors(self, pos: Position, allow_diagonal: bool = False) -> Iterator[Position]:
        r, c = pos
        orthogonal = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        directions = orthogonal + diagonal if allow_diagonal else orthogonal

        for dr, dc in directions:
            candidate = (r + dr, c + dc)
            if not self.is_walkable(candidate):
                continue
            if allow_diagonal and abs(dr) == 1 and abs(dc) == 1:
                # Prevent cutting through a wall corner diagonally.
                if not self.is_walkable((r + dr, c)) and not self.is_walkable((r, c + dc)):
                    continue
            yield candidate

    def copy(self) -> "Grid":
        return Grid.from_matrix(self.cells)

    def __str__(self) -> str:
        return "\n".join("".join("#" if v else "." for v in row) for row in self.cells)
