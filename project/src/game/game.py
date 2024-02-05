from __future__ import annotations
from ..utils.neighbors import hex_neighbors
from typing import Callable
from ..config import Config
from typing import Optional
from enum import Enum
import numpy as np
import tqdm


class BoardState(Enum):
    """Enum for the state of the board"""
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2


class PlayerOrder(Enum):
    """Enum for the players"""
    PLAYER1 = 1
    PLAYER2 = 2


MOVE_TYPE = tuple[int, int]


class Game:

    def __init__(self, config: Config, player_controllers: dict[str, Callable]) -> None:
        self.config = config
        self.player_controllers = player_controllers

        self.board = self.get_initial_board()
        self.over = False
        self.current_player = PlayerOrder.PLAYER1

        self.move_history: list[tuple[MOVE_TYPE, PlayerOrder]] = []
        self.undo_history: list[tuple[MOVE_TYPE, PlayerOrder]] = []

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

    def get_winner(self) -> Optional[PlayerOrder]:
        """Return the winner"""
        if self.over:
            return self.current_player
        return None
    
    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Return the valid moves"""
        moves = []
        for i in range(self.config.game.board_height):
            for j in range(self.config.game.board_width):
                if self.board[i, j] == BoardState.EMPTY:
                    moves.append((i, j))
        return moves

    # COMMANDS
    def update(self) -> None:
        """Update the game"""
        if self.over:
            return
        if len(self.move_history) == self.config.game.board_width * self.config.game.board_height:
            self.over = True
            return
        move = self.player_controllers[self.current_player.name](self)
        if move is None or self.board[move] != BoardState.EMPTY:
            return

        self.move_history.append((move, self.current_player))
        self.undo_history = []
        if self.current_player == PlayerOrder.PLAYER1:
            self.board[move] = BoardState.PLAYER1
        else:
            self.board[move] = BoardState.PLAYER2
        if self.__is_winning_move(move):
            self.over = True
            return
        # Comment this line to disable the switch player
        self.switch_player()

    def reset(self) -> None:
        """Reset the game"""
        self.board = self.get_initial_board()
        self.over = False
        self.current_player = PlayerOrder.PLAYER1
        self.move_history = []
        self.undo_history = []

    def run(self) -> None:
        """Run the game"""
        winner = {
            PlayerOrder.PLAYER1: 0,
            PlayerOrder.PLAYER2: 0
        }
        for _ in tqdm.tqdm(range(10000)):
            while not self.is_over():
                self.update()
            player_winner = self.get_winner()
            if player_winner:
                winner[player_winner] += 1
            self.reset()

        print(f"Player 1 won {winner[PlayerOrder.PLAYER1]} times")
        print(f"Player 2 won {winner[PlayerOrder.PLAYER2]} times")

    def undo(self) -> None:
        """Undo the last move"""
        if len(self.move_history) == 0:
            return
        move, player = self.move_history.pop()
        self.undo_history.append((move, player))
        self.board[move] = BoardState.EMPTY
        self.switch_player()

    def redo(self) -> None:
        """Redo the last move"""
        if len(self.undo_history) == 0:
            return
        move, player = self.undo_history.pop()
        self.current_player = player
        self.play(move)

    def play(self, move: tuple[int, int]) -> None:
        """Play a move"""
        self.move_history.append((move, self.current_player))
        if self.current_player == PlayerOrder.PLAYER1:
            self.board[move] = BoardState.PLAYER1
        else:
            self.board[move] = BoardState.PLAYER2
        if self.__is_winning_move(move):
            self.over = True
            return
        self.switch_player()

    def pass_turn(self) -> None:
        """Pass the turn"""
        self.switch_player()

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
            return self.__is_linked(move, currentColor, player, edges[1])
        # Else check if the move is connected to 2+ neighbors of the same color
        # (Can't win otherwise)
        multiple = False
        for neighbor in hex_neighbors(move, (self.config.game.board_width, self.config.game.board_height)):
            if self.board[neighbor] == currentColor:
                if multiple:
                    return self.__is_linked(move, currentColor, player, edges[1])
                multiple = True
        return False

    def __is_linked(self, move: tuple[int, int], currentColor: BoardState, player: int, size) -> bool:
        """Return True if the given move is linked to both sides"""
        cache = {}
        liste = set([move])
        edgeLink1, edgeLink2 = False, False
        while liste:
            current = liste.pop()
            if current in cache:
                continue
            cache[current] = True
            if current[player] == 0:
                edgeLink1 = True
            if current[player] == size:
                edgeLink2 = True
            if edgeLink1 and edgeLink2:
                return True
            for neighbor in hex_neighbors(current, (self.config.game.board_width, self.config.game.board_height)):
                if self.board[neighbor] == currentColor:
                    liste.add(neighbor)
        return False

    def switch_player(self) -> None:
        """Switch the current player"""
        other = {
            PlayerOrder.PLAYER1: PlayerOrder.PLAYER2,
            PlayerOrder.PLAYER2: PlayerOrder.PLAYER1
        }
        self.current_player = other[self.current_player]
    
    def copy(self) -> Game:
        """Return a copy of the game"""
        new_game = Game(self.config, self.player_controllers)
        new_game.board = self.board.copy()
        new_game.over = self.over
        new_game.current_player = self.current_player
        new_game.move_history = self.move_history.copy()
        new_game.undo_history = self.undo_history.copy()
        return new_game

    def get_value_and_terminated(self) -> tuple[float, bool]:
        """Return the value of the game and if it's terminated"""
        if self.over:
            return 1, True
        return 0, False