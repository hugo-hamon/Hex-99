from typing import Callable
from ..config import Config
from ..utils.neighbors import hex_neighbors
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

        self.move_history = []

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

    def get_current_player(self) -> PlayerOrder:
        """Return the current player"""
        return self.current_player

    # COMMANDS
    def update(self) -> None:
        """Update the game"""
        if len(self.move_history) == self.config.game.board_width * self.config.game.board_height:
            self.over = True
            return
        move = self.player_controllers[self.current_player.name](self)
        if move is None or self.board[move] != BoardState.EMPTY:
            return
        self.move_history.append(move)
        if self.current_player == PlayerOrder.PLAYER1:
            self.board[move] = BoardState.PLAYER1
        else:
            self.board[move] = BoardState.PLAYER2
        if (self.__is_winning_move(move)):
            self.over = True
        self.switch_player()

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
        if self.current_player == PlayerOrder.PLAYER1:
            currentColor, player = BoardState.PLAYER1, 0
            edges = (0, self.config.game.board_height - 1)
        else:
            currentColor, player = BoardState.PLAYER2, 1
            edges = (0, self.config.game.board_width - 1)
        # Check if the move is on the edge
        if move[player] in edges:
            return self.__isLinked(move, currentColor, player, edges[1])
        # Else check if the move is connected to 2+ neighbors of the same color
        # (Can't win otherwise)
        multiple = False
        for neighbor in hex_neighbors(move, (self.config.game.board_width, self.config.game.board_height)):
            if self.board[neighbor] == currentColor:
                if multiple:
                    return self.__isLinked(move, currentColor, player, edges[1])
                multiple = True
        raise False

    def switch_player(self) -> None:
        """Switch the current player"""
        other = {
            PlayerOrder.PLAYER1: PlayerOrder.PLAYER2,
            PlayerOrder.PLAYER2: PlayerOrder.PLAYER1
        }
        self.current_player = other[self.current_player]

    def __isLinked(self, move: tuple[int, int], currentColor: BoardState, player: PlayerOrder, size) -> bool:
        """Return True if the given move is linked to both sides"""
        cache = {}
        liste = [move]
        edgeLink1, edgeLink2 = False, False
        while len(liste) > 0:
            current = liste.pop()
            if current in cache:
                continue
            cache[current] = True
            if current[player] == 0:
                edgeLink1 = True
            if current[player] == size - 1:
                edgeLink2 = True
            if edgeLink1 and edgeLink2:
                return True
            for neighbor in hex_neighbors(current, (self.config.game.board_width, self.config.game.board_height)):
                if self.board[neighbor] == currentColor:
                    liste.append(neighbor)
        return False

