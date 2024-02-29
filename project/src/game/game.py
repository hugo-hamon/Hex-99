from __future__ import annotations
from .graph import GameGraphManager
from typing import Callable
from ..config import Config
from typing import Optional
from enum import Enum
import numpy as np
import cProfile
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

        self.graphs = GameGraphManager(config, self.config.game.allow_backtrack)
        
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
        return self.graphs.get_valid_moves()
    
    def get_move_history(self) -> list[tuple[MOVE_TYPE, PlayerOrder]]:
        """Return the move history"""
        return self.move_history

    # COMMANDS
    def update(self) -> None:
        """Update the game"""
        if self.over:
            return
        if len(self.move_history) == self.config.game.board_width * self.config.game.board_height:
            self.over = True
            return
        # test get move
        move = self.player_controllers[self.current_player.name](self)
        if move is None or self.board[move] != BoardState.EMPTY:
            return
        self.play(move)
        return

    def reset(self) -> None:
        """Reset the game"""
        self.board = self.get_initial_board()
        self.graphs = GameGraphManager(self.config, self.config.game.allow_backtrack)
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
        for _ in tqdm.tqdm(range(1000)):
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
        self.graphs.undo()

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
        self.graphs.update(move, 0 if self.current_player == PlayerOrder.PLAYER1 else 1)
        #if self.__is_winning_move(move):
        if self.graphs.has_won(0 if self.current_player == PlayerOrder.PLAYER1 else 1):
            self.over = True
            return
        self.switch_player()

    def pass_turn(self) -> None:
        """Pass the turn"""
        self.switch_player()

    def get_game_graphs(self):
        """Return the game graphs"""
        return self.graphs

    # UTILS
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
        new_game.graphs = self.graphs.copy()
        return new_game

    def get_value_and_terminated(self) -> tuple[float, bool]:
        """Return the value of the game and if it's terminated"""
        if self.over:
            return 1, True
        return 0, False