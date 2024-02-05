from .manager import Manager
from ..game.game import Game
from typing import Optional
from ..config import Config


class UserManager(Manager):

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.current_move = None

    def set_move(self, move: tuple[int, int]) -> None:
        """Set the current move"""
        self.current_move = move

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the current move"""
        if self.current_move is None:
            return None
        move = self.current_move
        self.current_move = None
        return move
    
    def reset(self) -> None:
        """Reset the manager"""
        self.current_move = None