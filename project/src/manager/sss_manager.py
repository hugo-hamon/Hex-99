from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple
from queue import PriorityQueue
from ..utils.node import Node
from enum import Enum

from ..utils.heuristics_func import Heuristic, evaluate
from ..game.game import Game, PlayerOrder
from ..utils.node import Node
from .manager import Manager
from ..config import Config


class State(Enum):
    LIVE = 1
    SOLVE = 2


@dataclass(order=True)
class PriorityQueueItem:
    priority: float
    node: Node = field(compare=False)
    state: State = field(compare=False)
    best_move: Optional[Tuple[int, int]] = field(compare=False)


class SSSManager(Manager):
    def __init__(self, config: Config, depth: int) -> None:
        super().__init__(config)
        self.depth = depth
        if depth < 1:
            raise ValueError("SSS* depth should be at least 1")

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

    def get_move(self, game: Game) -> Optional[Tuple[int, int]]:
        """Return the best move using the SSS* algorithm"""
        if move := self.check_for_winning_move(game):
            return move
        _, move = self.sss_star(game, self.depth, game.get_current_player())
        return move

    def sss_star(self, game: Game, depth: int, player: PlayerOrder) -> Tuple[float, Optional[Tuple[int, int]]]:
        """SSS* algorithm"""
        high_value = 1000
        root = Node(game, depth=depth)
        pq = PriorityQueue()
        pq.put(PriorityQueueItem(-high_value, root, State.LIVE, None))

        while not pq.empty():
            item = pq.get()
            h, node, state, best_move = item.priority, item.node, item.state, item.best_move
            if node.stale:
                continue
            if node == root and state == State.SOLVE:
                return -h, best_move
            if state == State.LIVE:
                if node.is_leaf():
                    evaluation = -(evaluate(node.get_game(), player, Heuristic.TWO_DISTANCE) + node.depth)
                    pq.put(PriorityQueueItem(max(evaluation, h), node, State.SOLVE, None))
                elif node.game.get_current_player() == player:
                    for child in node.expand():
                        pq.put(PriorityQueueItem(h, child, State.LIVE, None))
                else:
                    node.expand()
                    pq.put(PriorityQueueItem(h, node.children.pop(), State.LIVE, None))
            else:
                if node.game.get_current_player() != player:
                    pq.put(PriorityQueueItem(h, node.parent, State.SOLVE, node.last_move))
                    for child in node.parent.children:
                        child.stale = True
                else:
                    try:
                        pq.put(PriorityQueueItem(h, node.parent.children.pop(), State.LIVE, None))
                    except IndexError:
                        pq.put(PriorityQueueItem(h, node.parent, State.SOLVE, node.last_move))

        return 0, None


        
