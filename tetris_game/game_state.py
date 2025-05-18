class GameState:
    """Tracks the progress of a Tetris session."""

    def __init__(self) -> None:
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.next_tetromino = None
        self.lines_to_next_level = 10

    def add_score(self, lines_cleared: int) -> None:
        points = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
        self.score += points.get(lines_cleared, 0) * self.level
        self.lines_cleared += lines_cleared
        self.lines_to_next_level -= lines_cleared
        if self.lines_to_next_level <= 0:
            self.level += 1
            self.lines_to_next_level = 10

    def set_game_over(self, status: bool = True) -> None:
        self.game_over = status

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def set_next_tetromino(self, tetromino) -> None:
        self.next_tetromino = tetromino

    def get_fall_speed(self) -> float:
        return max(0.05, 1.0 - (self.level - 1) * 0.1)
