import random
from typing import Optional

import numpy as np

from .board import Board
from .block import Tetromino
from .config import TETROMINOES, TETROMINO_COLORS
from .game_state import GameState


class GameLogic:
    """Core gameplay mechanics."""

    def __init__(self, board: Board, game_state: GameState) -> None:
        self.board = board
        self.game_state = game_state
        self.current_tetromino: Optional[Tetromino] = None
        self.fall_time = 0.0
        self.fall_timer = 0.0
        self._spawn_new_tetromino()

    def _choose_random_shape(self) -> str:
        return random.choice(list(TETROMINOES.keys()))

    def _spawn_new_tetromino(self) -> None:
        name = self._choose_random_shape()
        shapes = [np.array(s) for s in TETROMINOES[name]]
        color = TETROMINO_COLORS[name]
        tetromino = Tetromino(name, shapes, color, x=self.board.width // 2 - 1, y=0)
        self.current_tetromino = tetromino
        self.game_state.set_next_tetromino(tetromino)

    def _move_tetromino(self, dx: int, dy: int) -> None:
        if not self.current_tetromino:
            return
        self.current_tetromino.move(dx, dy)
        if not self.board.is_valid_position(self.current_tetromino):
            self.current_tetromino.move(-dx, -dy)

    def _rotate_tetromino(self) -> None:
        if not self.current_tetromino:
            return
        self.current_tetromino.rotate()
        if not self.board.is_valid_position(self.current_tetromino):
            self.current_tetromino.rotate(clockwise=False)

    def _hard_drop(self) -> None:
        if not self.current_tetromino:
            return
        while self.board.is_valid_position(self.current_tetromino, offset_y=1):
            self.current_tetromino.move(0, 1)
        self._lock_and_prepare_next()

    def _lock_and_prepare_next(self) -> None:
        if not self.current_tetromino:
            return
        self.board.lock_tetromino(self.current_tetromino)
        lines = self.board.clear_completed_lines()
        self.game_state.add_score(lines)
        if self.board.is_game_over():
            self.game_state.set_game_over(True)
            return
        self._spawn_new_tetromino()

    def update(self, dt: float) -> None:
        if self.game_state.paused or self.game_state.game_over:
            return
        self.fall_timer += dt
        if self.fall_timer >= self.game_state.get_fall_speed():
            self.fall_timer = 0.0
            if self.board.is_valid_position(self.current_tetromino, offset_y=1):
                self.current_tetromino.move(0, 1)
            else:
                self._lock_and_prepare_next()

    def handle_input_action(self, action: str) -> None:
        if action == "MOVE_LEFT":
            self._move_tetromino(-1, 0)
        elif action == "MOVE_RIGHT":
            self._move_tetromino(1, 0)
        elif action == "SOFT_DROP":
            self._move_tetromino(0, 1)
        elif action == "ROTATE":
            self._rotate_tetromino()
        elif action == "HARD_DROP":
            self._hard_drop()
        elif action == "PAUSE":
            self.game_state.toggle_pause()
