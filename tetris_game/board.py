from __future__ import annotations

from typing import List

import numpy as np

from tetris_game.block import Tetromino
from tetris_game.config import BOARD_WIDTH, BOARD_HEIGHT


class Board:
    """Represents the game board state."""

    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT) -> None:
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)

    def is_valid_position(self, tetromino: Tetromino, offset_x: int = 0, offset_y: int = 0) -> bool:
        for x, y in tetromino.get_occupied_cells():
            new_x = x + offset_x
            new_y = y + offset_y
            if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
                return False
            if self.grid[new_y, new_x]:
                return False
        return True

    def lock_tetromino(self, tetromino: Tetromino) -> None:
        for x, y in tetromino.get_occupied_cells():
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

    def clear_completed_lines(self) -> int:
        lines_to_clear: List[int] = [i for i, row in enumerate(self.grid) if all(row)]
        if not lines_to_clear:
            return 0
        self.grid = np.delete(self.grid, lines_to_clear, axis=0)
        new_rows = np.zeros((len(lines_to_clear), self.width), dtype=int)
        self.grid = np.vstack((new_rows, self.grid))
        return len(lines_to_clear)

    def is_game_over(self) -> bool:
        return any(self.grid[0])

    def get_grid_state(self) -> np.ndarray:
        return self.grid.copy()
