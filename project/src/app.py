from .utils.manager_func import match_manager
from .manager.user_manager import UserManager
from .game.game import Game, PlayerOrder
from .manager.manager import Manager
from .config import load_config
from typing import Optional
import logging
import toml
import eel
import os

RUN_EPISODES = 10


class App:

    def __init__(self, config_path: str) -> None:
        self.config = load_config(config_path)

        self.player1: Optional[Manager] = None
        self.player2: Optional[Manager] = None

        self.game = None

    def run(self) -> None:
        """Run the app with the given config"""

        self.player1 = match_manager(
            self.config,
            self.config.user.player1_algorithm,
            self.config.user.player1_depth,
        )

        self.player2 = match_manager(
            self.config,
            self.config.user.player2_algorithm,
            self.config.user.player2_depth,
        )
        logging.info(
            f"Player 1 is using {self.config.user.player1_algorithm}"
            + f" and Player 2 is using {self.config.user.player2_algorithm}"
        )

        self.game = Game(
            self.config,
            {
                PlayerOrder.PLAYER1.name: self.player1.get_move,
                PlayerOrder.PLAYER2.name: self.player2.get_move,
            },
        )
        self.game.create_board()

        if self.config.graphics.graphics_enabled:
            eel.init("src/graphics/web")
            self.expose_functions()
            eel.start(
                "index.html",
                mode="firefox",
                cmdline_args=["--start-fullscreen"],
                shutdown_delay=3,
            )
        else:
            self.game.run(RUN_EPISODES)

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

    def eel_get_board(self) -> Optional[list[list[int]]]:
        """Return the board"""
        if self.game:
            return self.game.get_board().tolist()

    def eel_reset_game(self) -> None:
        """Reset the game"""
        if self.game:
            self.game.reset()
            if self.player1:
                self.player1.reset()
            if self.player2:
                self.player2.reset()

    def eel_undo(self) -> None:
        """Undo the last move"""
        if self.game:
            self.game.undo()

    def eel_pass_turn(self) -> None:
        """Pass the turn"""
        if self.game:
            self.game.pass_turn()

    def eel_exit(self) -> None:
        """Exit the game"""
        logging.info("Exiting the game")
        os._exit(0)

    def eel_load_config_from_file(self, filename: str) -> None:
        """Load the config"""
        try:
            self.config = load_config(f"config/{filename}")
            self.player1 = match_manager(
                self.config,
                self.config.user.player1_algorithm,
                self.config.user.player1_depth,
            )
            self.player2 = match_manager(
                self.config,
                self.config.user.player2_algorithm,
                self.config.user.player2_depth,
            )
            self.game = Game(
                self.config,
                {
                    PlayerOrder.PLAYER1.name: self.player1.get_move,
                    PlayerOrder.PLAYER2.name: self.player2.get_move,
                },
            )
            self.game.create_board()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")
        except Exception as e:
            raise e

    def eel_save_config(self, config: dict, filename: str) -> None:
        if config["user"]["player1_depth"] == None:
            config["user"]["player1_depth"] = 0
        if config["user"]["player2_depth"] == None:
            config["user"]["player2_depth"] = 0
        if config["game"]["board_width"] == None:
            config["game"]["board_width"] = 0
        if config["game"]["board_height"] == None:
            config["game"]["board_height"] = 0

        config["graphics"] = {"graphics_enabled": True}

        with open(f"config/{filename}.toml", "w") as f:
            toml.dump(config, f)
