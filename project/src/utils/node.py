from __future__ import annotations
from ..game.game import MOVE_TYPE
from ..game.game import Game
from typing import Optional


class Node:

    def __init__(self, game: Game, parent: Optional[Node] = None, last_move: Optional[MOVE_TYPE] = None, depth: int = 0) -> None:
        self.game = game
        self.children = []
        self.parent = parent
        self.last_move = last_move
        self.depth = depth
        self.stale = False

    # Requests
    def get_game(self) -> Game:
        """Return the game of the node"""
        return self.game

    def get_parent(self) -> Optional[Node]:
        """Return the value of the node"""
        return self.parent

    def get_children(self) -> list[Node]:
        """Return the childrens of the node"""
        return self.children
    
    def is_leaf(self) -> bool:
        """Check if the node is a leaf node."""
        return self.depth == 0 or self.game.is_over()

    # Command
    def expand(self) -> list[Node]:
        """Return all possible children of the node"""
        for move in self.game.get_turbo_valid_moves(self.game.get_current_player()):
            game_copy = self.game.copy()
            game_copy.move(move)
            self.children.append(Node(game_copy, self, move, self.depth - 1))
        return self.children

    # Utils
    def get_tree_size(self) -> int:
        """Return the size of the tree"""
        size = 1
        for child in self.children:
            size += child.get_tree_size()
        return size

    def __lt__(self, other: Node) -> bool:
        return False
