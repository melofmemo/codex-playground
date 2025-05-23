"""Entry point for running the Tetris game."""

try:
    import pygame
except Exception:  # pragma: no cover - pygame may not be available
    pygame = None

from tetris_game.board import Board
from tetris_game.game_state import GameState
from tetris_game.game_logic import GameLogic
from tetris_game.input_handler import InputHandler
from tetris_game.renderer import Renderer
from tetris_game.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main() -> None:
    if not pygame:
        raise RuntimeError("pygame is not available in this environment")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    board = Board()
    state = GameState()
    logic = GameLogic(board, state)
    renderer = Renderer(screen)
    input_handler = InputHandler()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for action in input_handler.handle_input():
            if action == "QUIT":
                running = False
            else:
                logic.handle_input_action(action)
        logic.update(dt)
        renderer.render_all(board, logic.current_tetromino, (100, 50))

    pygame.quit()


if __name__ == "__main__":
    main()
