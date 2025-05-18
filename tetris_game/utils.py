"""Miscellaneous utility helpers for Tetris."""

from typing import Iterable

import numpy as np


def rotate_matrix_cw(matrix: Iterable[Iterable[int]]) -> np.ndarray:
    """Rotate a 2D matrix clockwise."""
    arr = np.array(list(matrix))
    return np.rot90(arr, k=-1)
