from abc import ABC, abstractmethod
from ..game.game import Game
from typing import Optional


class Manager(ABC):

    @abstractmethod
    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return a direction for a given algorithm"""
        return NotImplemented
