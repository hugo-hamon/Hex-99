from typing import Callable
from ..config import Config
from enum import Enum
import numpy as np


class BoardState(Enum):
    """Enum for the state of the board"""
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2


class PlayerOrder(Enum):
    """Enum for the players"""
    PLAYER1 = 1
    PLAYER2 = 2


class Game:

    def __init__(self, config: Config, player_controllers: dict[str, Callable]) -> None:
        self.config = config
        self.player_controllers = player_controllers

        self.board = self.get_initial_board()
        self.over = False
        self.current_player = PlayerOrder.PLAYER1

    # REQUESTS
    def get_board(self) -> np.ndarray:
        """Return the board"""
        return self.board

    def get_initial_board(self) -> np.ndarray:
        """Return an initial board given the config"""
        board_width = self.config.game.board_width
        board_height = self.config.game.board_height

        return np.full((board_height, board_width), BoardState.EMPTY)

    def is_over(self) -> bool:
        """Return True if the game is over"""
        return self.over

    # COMMANDS
    def update(self) -> None:
        """Update the game"""
        raise NotImplementedError

    def reset(self) -> None:
        """Reset the game"""
        raise NotImplementedError

    def run(self) -> None:
        """Run the game"""
        while not self.is_over():
            self.update()

    # UTILS
    def __is_winning_move(self, move: tuple[int, int]) -> bool:
        """Return True if the given move is a winning move"""
        raise NotImplementedError
