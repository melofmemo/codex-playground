import numpy as np
from tetris_game.board import Board
from tetris_game.block import Tetromino


def test_line_clear():
    board = Board(width=4, height=4)
    board.grid[3] = np.array([1, 1, 1, 1])
    shapes = [np.array([[1]])]
    tetro = Tetromino('O', shapes, (0, 0, 0), x=0, y=0)
    board.lock_tetromino(tetro)
    lines = board.clear_completed_lines()
    assert lines == 1
    assert board.grid[-1].sum() == 1
