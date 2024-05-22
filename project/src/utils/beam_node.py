from __future__ import annotations
from .node import Node
from ..game.game import Game
from typing import Optional
from .heuristics_func import Heuristic, evaluate

class BeamNode(Node):
    # TODO Implement beamsize in config
    def __init__(self, game: Game, value: float, children: Optional[list[Node]] = None) -> None:
        super().__init__(game, value, children)
        self.beam_width = 6
        if self.beam_width < 1:
            raise ValueError("Beam width should be at least 1")
    
    def expand(self) -> list[Node]:
        """Return all possible children of the node"""
        for move in self.game.get_valid_moves(self.game.get_current_player()):
            game_copy = self.game.copy()
            game_copy.move(move)
            self.children.append(BeamNode(game_copy, evaluate(game_copy, game_copy.get_current_player(), Heuristic.TWO_DISTANCE)))
        self.children = sorted(self.children, key=lambda x: x.get_value(), reverse=True)[:self.beam_width]
        return self.children