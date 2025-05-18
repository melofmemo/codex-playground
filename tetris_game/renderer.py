from typing import Tuple

try:
    import pygame
except Exception:  # pragma: no cover - pygame may not be available
    pygame = None

from tetris_game.config import GRID_SIZE, COLORS


class Renderer:
    """Draws the board and UI using pygame."""

    def __init__(self, surface) -> None:
        self.surface = surface

    def draw_grid(self, board_offset_x: int, board_offset_y: int, board_w_pixels: int, board_h_pixels: int) -> None:
        if not pygame:
            return
        for x in range(board_offset_x, board_offset_x + board_w_pixels, GRID_SIZE):
            pygame.draw.line(self.surface, COLORS['white'], (x, board_offset_y), (x, board_offset_y + board_h_pixels))
        for y in range(board_offset_y, board_offset_y + board_h_pixels, GRID_SIZE):
            pygame.draw.line(self.surface, COLORS['white'], (board_offset_x, y), (board_offset_x + board_w_pixels, y))

    def draw_board(self, board, board_offset_x: int, board_offset_y: int) -> None:
        if not pygame:
            return
        for y, row in enumerate(board.grid):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(board_offset_x + x * GRID_SIZE, board_offset_y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(self.surface, COLORS['white'], rect)

    def draw_tetromino(self, tetromino, board_offset_x: int, board_offset_y: int) -> None:
        if not pygame or not tetromino:
            return
        for x, y in tetromino.get_occupied_cells():
            rect = pygame.Rect(board_offset_x + x * GRID_SIZE, board_offset_y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.surface, tetromino.color, rect)

    def render_all(self, board, current_tetromino, board_offset: Tuple[int, int]) -> None:
        if not pygame:
            return
        board_offset_x, board_offset_y = board_offset
        board_w_pixels = board.width * GRID_SIZE
        board_h_pixels = board.height * GRID_SIZE
        self.surface.fill(COLORS['black'])
        self.draw_grid(board_offset_x, board_offset_y, board_w_pixels, board_h_pixels)
        self.draw_board(board, board_offset_x, board_offset_y)
        self.draw_tetromino(current_tetromino, board_offset_x, board_offset_y)
        pygame.display.flip()
