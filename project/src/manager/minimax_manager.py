from ..utils.heuristics_func import Heuristic, evaluate
from ..game.game import Game, PlayerOrder
from .manager import Manager
from typing import Optional
from ..config import Config


class MinimaxManager(Manager):

    def __init__(self, config: Config, depth: int) -> None:
        super().__init__(config)
        self.depth = depth
        if depth < 1:
            raise ValueError("Minimax depth should be at least 1")

    def reset(self) -> None:
        """Reset the manager"""
        pass

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the best move using the minimax algorithm"""
        return self.minimax(
            game, self.depth, True, game.get_current_player()
        )[1]

    def minimax(self, game: Game, depth: int, maximizing_player: bool, player: PlayerOrder) -> tuple[float, Optional[tuple[int, int]]]:
        """Minimax algorithm"""
        if depth == 0 or game.is_over():
            return evaluate(game, player, Heuristic.A_STAR), None

        best_move = None

        if maximizing_player:
            value = float('-inf')
            for move in game.get_valid_moves(game.get_current_player()):
                game_copy = game.copy()
                game_copy.move(move)
                move_value, _ = self.minimax(
                    game_copy, depth - 1, False, player
                )
                if move_value > value:
                    value = move_value
                    best_move = move
        else:
            value = float('inf')
            for move in game.get_valid_moves(game.get_current_player()):
                game_copy = game.copy()
                game_copy.move(move)
                move_value, _ = self.minimax(
                    game_copy, depth - 1, True, player
                )
                if move_value < value:
                    value = move_value
                    best_move = move

        return value, best_move
