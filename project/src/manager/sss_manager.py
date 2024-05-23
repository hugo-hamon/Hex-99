from __future__ import annotations
from ..utils.heuristics_func import Heuristic, evaluate
from ..game.game import Game, PlayerOrder
from typing import Optional, Tuple
from queue import PriorityQueue
from .manager import Manager
from ..config import Config


class SSSManager(Manager):

    def __init__(self, config: Config, depth: int) -> None:
        super().__init__(config)
        self.depth = depth
        if depth < 1:
            raise ValueError("SSS* depth should be at least 1")

    def reset(self) -> None:
        """Reset the manager"""
        pass

    def check_for_winning_move(self, game: Game) -> Optional[Tuple[int, int]]:
        """Check if there is a winning move in the current game state"""
        for move in game.get_valid_moves(game.get_current_player()):
            game_copy = game.copy()
            game_copy.move(move)
            if game_copy.is_over():
                return move
        return None

    def get_move(self, game: Game) -> Optional[Tuple[int, int]]:
        """Return the best move using the SSS* algorithm"""
        return self.sss_star(game, self.depth, game.get_current_player())

    def sss_star(
        self, game: Game, depth: int, player: PlayerOrder
    ) -> Optional[Tuple[int, int]]:
        """SSS* algorithm implementation"""
        pass
            
