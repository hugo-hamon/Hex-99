from ..game.game import Game, BoardState
from .manager import Manager
from typing import Optional
from ..config import Config
from random import choice
import random


class RandomManager(Manager):

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.moves = None
        self.index = 0

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the current move"""
        if not self.moves:
            self.moves = game.get_valid_moves()
            random.shuffle(self.moves)
            self.index = 0

        move = self.moves[self.index]
        board = game.get_board()
        while board[move] != BoardState.EMPTY:
            self.index += 1
            if self.index >= len(self.moves):
                self.moves = None
                return None
            move = self.moves[self.index]
        self.index += 1
        return move
    
    def reset(self) -> None:
        """Reset the manager"""
        self.moves = None
        self.index = 0