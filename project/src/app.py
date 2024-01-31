from .game.game import Game, BoardState, PlayerOrder
from .utils.manager_func import match_manager
from .manager.user_manager import UserManager
from .manager.manager import Manager
from .config import load_config
from typing import Optional
import numpy as np
import logging
import eel


class App:

    def __init__(self, config_path: str) -> None:
        self.config = load_config(config_path)

        self.player1: Optional[Manager] = None
        self.player2: Optional[Manager] = None

        self.game = None

    def run(self) -> None:
        """Run the app with the given config"""

        self.player1 = match_manager(
            self.config, self.config.user.player1_algorithm
        )

        self.player2 = match_manager(
            self.config, self.config.user.player2_algorithm
        )
        logging.info(
            f"Player 1 is using {self.config.user.player1_algorithm}" +
            f" and Player 2 is using {self.config.user.player2_algorithm}"
        )

        self.game = Game(
            self.config, {
                PlayerOrder.PLAYER1.name: self.player1.get_move,
                PlayerOrder.PLAYER2.name: self.player2.get_move
            }
        )

        if self.config.graphics.graphics_enabled:
            eel.init("src/graphics/web")
            self.expose_functions()
            eel.start(
                "index.html",
                mode="firefox",
                cmdline_args=["--start-fullscreen"],
                shutdown_delay=3
            )
        else:
            self.game.run()

    def expose_functions(self) -> None:
        """Expose functions to JavaScript"""
        functions = self.__dir__()
        for function in functions:
            if function.startswith("eel_"):
                eel.expose(getattr(self, function))

    # eel functions
    def eel_set_player_move(self, player: int, x: int, y: int) -> None:
        """Set the player move"""
        if player == 1 and isinstance(self.player1, UserManager):
            self.player1.set_move((x, y))
        elif player == 2 and isinstance(self.player2, UserManager):
            self.player2.set_move((x, y))

    def eel_get_current_player(self) -> Optional[int]:
        """Return the current player"""
        if self.game:
            return self.game.get_current_player().value

    def eel_is_game_over(self) -> Optional[bool]:
        """Return True if the game is over"""
        if self.game:
            return self.game.is_over()

    def eel_get_winner(self) -> Optional[str]:
        """Return the winner"""
        if self.game:
            winner = self.game.get_winner()
            if winner:
                return winner.name

    def eel_update_game(self) -> None:
        """Update the game"""
        if self.game:
            self.game.update()

    def eel_is_current_player_human(self) -> Optional[bool]:
        """Return True if the other player is human"""
        if self.game:
            if self.game.get_current_player() == PlayerOrder.PLAYER1:
                return isinstance(self.player1, UserManager)
            else:
                return isinstance(self.player2, UserManager)

    def eel_get_board(self) -> Optional[list[list[BoardState]]]:
        """Return the board"""
        if self.game:
            board = self.game.get_board().tolist()
            for row in board:
                for i, cell in enumerate(row):
                    row[i] = cell.value
            return board
