from __future__ import annotations
from ..game.game import Game, BoardState
from .manager import Manager
from typing import Optional
from ..config import Config
from random import shuffle, choice
import numpy as np
import math


class MCTSManager(Manager):

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the current move"""
        pass

    def reset(self) -> None:
        """Reset the manager"""
        pass
