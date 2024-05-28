from ..game.game import Game
from .manager import Manager
from typing import Optional
from ..config import Config
from random import choice


class RandomManager(Manager):

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the current move"""
        current_player = game.get_current_player()
        available_moves = game.get_valid_moves(current_player)
        return choice(available_moves)
    
    def reset(self) -> None:
        """Reset the manager"""
        pass