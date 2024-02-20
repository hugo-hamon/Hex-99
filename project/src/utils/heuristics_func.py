from ..game.game import Game, PlayerOrder
from enum import Enum
import random


class Heuristic(Enum):
    """Enum for the heuristics"""
    RANDOM = "random"  # Return a random value between -1 and 1


def evaluate(game: Game, player: PlayerOrder, heuristic: Heuristic) -> float:
    """Return a value for the given game state using the given heuristic"""
    if heuristic == Heuristic.RANDOM:
        return random_heuristic()
    return 0.0


def random_heuristic() -> float:
    """Return a random value between -1 and 1"""
    return random.uniform(-1, 1)
