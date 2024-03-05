from ..utils.heuristics_func import Heuristic, evaluate
from ..utils.node import Node
from .manager import Manager
from ..game.game import Game
from ..config import Config
from typing import Optional
import logging


class AlphaBetaManager(Manager):

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        if self.config.alpha_beta.depth < 1:
            raise ValueError("AlphaBeta depth should be at least 1")

    def reset(self) -> None:
        """Reset the manager"""
        pass

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the best move using the alpha beta algorithm"""
        tree = self.alpha_beta_build_tree(game, self.config.alpha_beta.depth, float('-inf'), float('inf'), True)
        best_move = None
        best_value = float('-inf')

        logging.info(f"AlphaBeta Tree size: {tree.get_tree_size()}")

        for child in tree.get_children():
            if child.get_value() > best_value:
                best_value = child.get_value()
                best_move = child.get_game().get_move_history()[-1][1]
        return best_move


    def alpha_beta_build_tree(self, game: Game, depth: int, alpha: float, beta: float, maximizing_player: bool) -> Node:
        """Build a partial tree using alpha-beta pruning"""
        if depth == 0 or game.is_over():
            return Node(game, evaluate(game, game.get_current_player(), Heuristic.TWO_DISTANCE))
        
        node = Node(game, 0)
        if maximizing_player:
            value = float('-inf')
            for move in game.get_valid_moves(game.get_current_player()):
                game_copy = game.copy()
                game_copy.move(move)
                child = self.alpha_beta_build_tree(game_copy, depth - 1, alpha, beta, False)
                value = max(value, child.get_value())
                alpha = max(alpha, value)
                if beta <= alpha and alpha != float('inf'):
                    break
                node.add_child(child)
            node.set_value(value)
            return node
        else:
            value = float('inf')
            for move in game.get_valid_moves(game.get_current_player()):
                game_copy = game.copy()
                game_copy.move(move)
                child = self.alpha_beta_build_tree(game_copy, depth - 1, alpha, beta, True)
                value = min(value, child.get_value())
                beta = min(beta, value)
                if beta <= alpha and beta != float('-inf'):
                    break
                node.add_child(child)
            node.set_value(value)
            return node