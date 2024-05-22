from src.game.game import Game, PlayerOrder
from src.config import load_config
from src.utils.heuristics_func import *
import logging
import sys
import os

LOGGING_CONFIG = {
    'level': logging.INFO,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%d-%b-%y %H:%M:%S',
    'filename': 'log/log.log',
    'filemode': 'w'
}

DEFAULT_CONFIG_PATH = "config/default.toml"

if __name__ == "__main__":
    if not os.path.exists("log"):
        os.makedirs("log")

    logging.basicConfig(**LOGGING_CONFIG)
    logging.info("Starting run.py")

    argv = len(sys.argv)
    path = DEFAULT_CONFIG_PATH
    if argv == 2:
        path = sys.argv[1]
        path = f"config/{path}.toml"
        logging.info(f"Using config path : {path}")
    else:
        logging.info(f"Using default config path : {path}")
    config = load_config(path)
    game = Game(config, None)
    game.create_board()
    game.move((1, 2))
    game.move((1, 3))
    game.move((3, 1))
    game.move((1, 4))
    game.draw_graph(PlayerOrder.PLAYER1)
    game.draw_graph(PlayerOrder.PLAYER2)
    two_distance(game, PlayerOrder.PLAYER1)