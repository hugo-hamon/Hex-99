from ..game.game import Game, BoardState
from .manager import Manager
from typing import Optional
from ..config import Config
from random import choice


class RandomManager(Manager):

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the current move"""
        board = game.get_board()
        available_moves = []
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i, j] == BoardState.EMPTY:
                    available_moves.append((i, j))
        return choice(available_moves)
    
    def reset(self) -> None:
        """Reset the manager"""
        pass