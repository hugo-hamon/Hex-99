from ..utils.heuristics_func import Heuristic, evaluate
from ..utils.neighbors import hex_neighbors
from ..game.game import Game, BoardState
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

    def reset(self) -> None:
        """Reset the manager"""
        pass

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the current move"""
        tree = self.build_tree(game, self.config.minimax.depth)
        self.minimax(tree, self.config.minimax.depth, True)
        best_move = None
        best_value = float('-inf')
        logging.info(f"Minimax Tree size: {tree.get_tree_size()}")
        for child in tree.get_children():
            if child.get_value() > best_value:
                best_value = child.get_value()
                best_move = child.get_game().get_move_history()[-1][0]
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
        for move in game.get_valid_moves():
            game_copy = game.copy()
            game_copy.play(move)
            children.append(self.build_tree(game_copy, depth - 1))
        return Node(game, 0, children)

    def get_less_valid_moves(self, game: Game) -> list[tuple[int, int]]:
        """Return valid moves"""
        if len(game.get_move_history()) == 0:
            return [(game.get_board().shape[0] // 2, game.get_board().shape[1] // 2)]

        valid_moves = game.get_valid_moves()
        new_valid_moves = []
        game_board = game.get_board()
        for move in valid_moves:
            neighbors = hex_neighbors(move, self.config)
            for neighbor in neighbors:
                if game_board[neighbor] != BoardState.EMPTY:
                    new_valid_moves.append(move)
                    break
        if len(new_valid_moves) == 0:
            return valid_moves
        return new_valid_moves
