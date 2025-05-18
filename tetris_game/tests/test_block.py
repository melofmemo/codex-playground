import numpy as np
from tetris_game.block import Tetromino


def test_rotation():
    shapes = [np.array([[1, 0], [1, 1]]), np.array([[1, 1], [1, 0]])]
    t = Tetromino('S', shapes, (0, 0, 0))
    assert t.current_shape[0, 0] == 1
    t.rotate()
    assert (t.current_shape == shapes[1]).all()
    t.rotate(clockwise=False)
    assert (t.current_shape == shapes[0]).all()
