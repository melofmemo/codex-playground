from typing import List

try:
    import pygame
except Exception:  # pragma: no cover - pygame may not be available
    pygame = None


class InputHandler:
    """Translate pygame events into game actions."""

    KEY_ACTIONS = {
        pygame.K_LEFT if pygame else -1: "MOVE_LEFT",
        pygame.K_RIGHT if pygame else -1: "MOVE_RIGHT",
        pygame.K_DOWN if pygame else -1: "SOFT_DROP",
        pygame.K_UP if pygame else -1: "ROTATE",
        pygame.K_SPACE if pygame else -1: "HARD_DROP",
        pygame.K_p if pygame else -1: "PAUSE",
    }

    def handle_input(self) -> List[str]:
        if not pygame:
            return []
        actions: List[str] = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append("QUIT")
            elif event.type == pygame.KEYDOWN:
                action = self.KEY_ACTIONS.get(event.key)
                if action:
                    actions.append(action)
        return actions
