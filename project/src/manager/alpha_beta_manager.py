from ..utils.heuristics_func import Heuristic, evaluate
from ..game.game import Game, PlayerOrder
from ..utils.node import Node
from .manager import Manager
from ..config import Config
from typing import Optional
import logging


class AlphaBetaManager(Manager):

    def __init__(self, config: Config, depth: int) -> None:
        super().__init__(config)
        self.depth = depth
        if depth < 1:
            raise ValueError("AlphaBeta depth should be at least 1")

    def reset(self) -> None:
        """Reset the manager"""
        pass

    def check_for_winning_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Check if there is a winning move in the current game state"""
        for move in game.get_valid_moves(game.get_current_player()):
            game_copy = game.copy()
            game_copy.move(move)
            if game_copy.is_over():
                return move
        return None

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the best move using the alpha beta algorithm"""
        return self.alphabeta(
            game, self.depth, float('-inf'), float('inf'),
            True, game.get_current_player()
        )[1]

    def alphabeta(self, game: Game, depth: int, alpha: float, beta: float, maximizing_player: bool, player: PlayerOrder) -> tuple[float, Optional[tuple[int, int]]]:
        """Alpha-beta pruning algorithm"""
        if depth == 0 or game.is_over():
            return evaluate(game, player, Heuristic.TWO_DISTANCE), None

        best_move = None

        if maximizing_player:
            value = float('-inf')
            for move in game.get_turbo_valid_moves(game.get_current_player()):
                game_copy = game.copy()
                game_copy.move(move)
                move_value, _ = self.alphabeta(
                    game_copy, depth - 1, alpha, beta, False, player
                )
                if move_value > value:
                    value = move_value
                    best_move = move
                alpha = max(alpha, value)
                if value >= beta:
                    break
        else:
            value = float('inf')
            for move in game.get_valid_moves(game.get_current_player()):
                game_copy = game.copy()
                game_copy.move(move)
                move_value, _ = self.alphabeta(
                    game_copy, depth - 1, alpha, beta, True, player
                )
                if move_value < value:
                    value = move_value
                    best_move = move
                beta = min(beta, value)
                if value <= alpha:
                    break
        
        return value, best_move
