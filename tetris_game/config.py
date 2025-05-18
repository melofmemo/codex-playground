# Configuration constants for the Tetris game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
FPS = 60

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Basic RGB color tuples
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'cyan': (0, 255, 255),
    'yellow': (255, 255, 0),
    'purple': (160, 32, 240),
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'orange': (255, 165, 0),
}

# Tetromino rotation states expressed as lists of matrices
TETROMINOES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]],
    ],
    'O': [
        [[1, 1], [1, 1]],
    ],
    'T': [
        [[0, 1, 0], [1, 1, 1]],
        [[1, 0], [1, 1], [1, 0]],
        [[1, 1, 1], [0, 1, 0]],
        [[0, 1], [1, 1], [0, 1]],
    ],
    'S': [
        [[0, 1, 1], [1, 1, 0]],
        [[1, 0], [1, 1], [0, 1]],
    ],
    'Z': [
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1], [1, 1], [1, 0]],
    ],
    'J': [
        [[1, 0, 0], [1, 1, 1]],
        [[1, 1], [1, 0], [1, 0]],
        [[1, 1, 1], [0, 0, 1]],
        [[0, 1], [0, 1], [1, 1]],
    ],
    'L': [
        [[0, 0, 1], [1, 1, 1]],
        [[1, 0], [1, 0], [1, 1]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1], [0, 1], [0, 1]],
    ],
}

TETROMINO_COLORS = {
    'I': COLORS['cyan'],
    'O': COLORS['yellow'],
    'T': COLORS['purple'],
    'S': COLORS['green'],
    'Z': COLORS['red'],
    'J': COLORS['blue'],
    'L': COLORS['orange'],
}
