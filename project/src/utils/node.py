from __future__ import annotations
from ..game.game import Game
from typing import Optional


class Node:

    def __init__(self, game: Game, parent: Optional[Node] = None, last_move: Optional[Node] = None, depth: int = 0) -> None:
        self.game = game
        self.alive = True
        self.children = []
        self.parent = parent
        self.last_move = last_move
        self.depth = depth
        self.stale = False

    # Requests
    def get_game(self) -> Game:
        """Return the game of the node"""
        return self.game

    def get_parent(self) -> Node:
        """Return the value of the node"""
        return self.value

    def get_children(self) -> list[Node]:
        """Return the childrens of the node"""
        return self.parent

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
    
    def display(self, depth: int = 0) -> None:
        """Display the tree"""
        print(f"{' ' * depth}{self.game.get_move_history()[-1][1]}: {self.value}")
        for child in self.children:
            child.display(depth + 1)

    def __lt__(self, other: Node) -> bool:
        return False
