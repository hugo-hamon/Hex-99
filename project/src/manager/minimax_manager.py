from ..utils.heuristics_func import Heuristic, evaluate
from ..game.game import Game, PlayerOrder
from ..utils.node import Node
from .manager import Manager
from typing import Optional
from ..config import Config
import logging


class MinimaxManager(Manager):

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        if self.config.minimax.depth < 1:
            raise ValueError("Minimax depth should be at least 1")

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the best move using the minimax algorithm"""
        tree = self.build_tree(game, self.config.minimax.depth)
        self.minimax(tree, self.config.minimax.depth, True)
        best_move = None
        best_value = float('-inf')
        logging.info(f"Minimax Tree size: {tree.get_tree_size()}")

        for child in tree.get_children():
            if child.get_value() > best_value:
                best_value = child.get_value()
                best_move = child.get_game().get_move_history()[-1][1]
        return best_move

    def minimax(self, node: Node, depth: int, maximizing_player: bool) -> float:
        """Update the value of the node using the minimax algorithm"""
        if depth == 0 or node.get_game().is_over():
            return node.get_value()

        if maximizing_player:
            value = float('-inf')
            for child in node.get_children():
                value = max(value, self.minimax(child, depth - 1, False))
            node.set_value(value)
            return value
        else:
            value = float('inf')
            for child in node.get_children():
                value = min(value, self.minimax(child, depth - 1, True))
            node.set_value(value)
            return value

    def build_tree(self, game: Game, depth: int) -> Node:
        """Return a tree with the given depth"""
        if depth == 0 or game.is_over():
            return Node(game, evaluate(game, game.get_current_player(), Heuristic.TWO_DISTANCE))
        children = []
        for move in game.get_valid_moves(game.get_current_player()):
            game_copy = game.copy()
            game_copy.move(move)
            children.append(self.build_tree(game_copy, depth - 1))
        return Node(game, 0, children)

    def reset(self) -> None:
        """Reset the manager"""
        pass
