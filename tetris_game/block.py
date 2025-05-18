from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


@dataclass
class Tetromino:
    """Represents a falling Tetris block."""

    shape_name: str
    shapes: List[np.ndarray]
    color: Tuple[int, int, int]
    x: int = 0
    y: int = 0
    rotation_index: int = 0

    @property
    def current_shape(self) -> np.ndarray:
        return self.shapes[self.rotation_index]

    def rotate(self, clockwise: bool = True) -> None:
        if clockwise:
            self.rotation_index = (self.rotation_index + 1) % len(self.shapes)
        else:
            self.rotation_index = (self.rotation_index - 1) % len(self.shapes)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def get_occupied_cells(self) -> List[Tuple[int, int]]:
        cells = []
        shape = self.current_shape
        for row_idx, row in enumerate(shape):
            for col_idx, val in enumerate(row):
                if val:
                    cells.append((self.x + col_idx, self.y + row_idx))
        return cells
