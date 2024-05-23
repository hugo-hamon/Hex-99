from __future__ import annotations
from ..game.game import Game
from typing import Optional


class Node:

    def __init__(self, game: Game, value: float, children: Optional[list[Node]] = None) -> None:
        self.game = game
        self.value = value
        if children is None:
            children = []
        self.children = children
        self.parent = None

    # Request
    def get_game(self) -> Game:
        """Return the game of the node"""
        return self.game

    def get_value(self) -> float:
        """Return the value of the node"""
        return self.value

    def get_children(self) -> list[Node]:
        """Return the childrens of the node"""
        return self.children

    # Command
    def set_game(self, game: Game) -> None:
        """Set the game of the node"""
        self.game = game

    def add_child(self, child: Node) -> None:
        """Add a child to the node"""
        self.children.append(child)

    def set_value(self, value: float) -> None:
        """Set the value of the node"""
        self.value = value

    def expand(self) -> list[Node]:
        """Return all possible children of the node"""
        for move in self.game.get_valid_moves(self.game.get_current_player()):
            game_copy = self.game.copy()
            game_copy.move(move)
            self.children.append(Node(game_copy, 0))    
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
