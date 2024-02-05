from __future__ import annotations
from ..game.game import Game
from .manager import Manager
from typing import Optional
from ..config import Config
import numpy as np
import random
import math


class MCTSManager(Manager):

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the current move"""
        raise NotImplementedError