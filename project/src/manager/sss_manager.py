from __future__ import annotations
from typing import Optional, Tuple
from queue import PriorityQueue

from ..utils.heuristics_func import Heuristic, evaluate
from ..game.game import Game, PlayerOrder
from ..utils.node import Node
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
        for move in game.get_turbo_valid_moves(game.get_current_player()):
            game_copy = game.copy()
            game_copy.move(move)
            if game_copy.is_over():
                return move
        return None

    def get_move(self, game: Game) -> Optional[Tuple[int, int]]:
        """Return the best move using the SSS* algorithm"""
        return self.sss_star(game, self.depth, game.get_current_player())[1]

    def sss_star(
        self, game: Game, depth: int, player: PlayerOrder
    ) -> Optional[Tuple[int, int]]:
        """SSS* algorithm implementation"""
        if depth == 0 or game.is_over():
            return evaluate(game, player, Heuristic.TWO_DISTANCE) + depth, None
        
        high_value = 1000
        best_move = None
        root = Node(game, depth=depth)
        queue = PriorityQueue()
        queue.put((-high_value, root, best_move))
        while queue:
            t = queue.get()
            value, current_node, best_move = t
            if current_node.stale:
                continue
            #print(current_node)
            if current_node.parent is None and not current_node.alive:
                #print("END")
                #print(best_move)
                return -value, best_move
            if current_node.alive:
                #print("Alive")
                if current_node.depth == 0 or current_node.get_game().is_over():
                    #print("Leaf")
                    current_node.alive = False
                    new_value = max(value, -(evaluate(current_node.get_game(), player, Heuristic.TWO_DISTANCE) + current_node.depth))
                    queue.put((new_value, current_node, None))
                else:
                    #print("Not leaf")
                    if current_node.game.get_current_player() == player:
                        #print("Max")
                        current_node.expand()
                        for child in current_node.children:
                            queue.put((value, child, None))
                    else:
                        #print("Min")
                        current_node.expand()
                        queue.put((value, current_node.children.pop(), None))
            else:
                #print("Dead")
                if current_node.game.get_current_player() != player:
                    #print("Min")
                    current_node.parent.alive = False
                    queue.put((value, current_node.parent, current_node.last_move))
                    for node in current_node.parent.children:
                        node.stale = True
                else:
                    #print("Max")
                    try:
                        queue.put((value, current_node.parent.children.pop(), None))
                    except IndexError:
                        current_node.parent.alive = False
                        queue.put((value, current_node.parent, current_node.last_move))



            


            
