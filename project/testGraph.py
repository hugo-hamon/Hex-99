from src.game.game import Game, PlayerOrder
from src.config import load_config
from src.utils.heuristics_func import *
from dataclasses import dataclass, field
from queue import PriorityQueue
import numpy as np
import logging
import sys
import os


@dataclass(order=True)
class PriorityQueueItem:
    priority: float
    value: int = field(compare=False)



queue = PriorityQueue()
queue.put(PriorityQueueItem(0, 1))
queue.put(PriorityQueueItem(0, 2))

print(queue.get())
queue.put(PriorityQueueItem(0, 1))
print(queue.get())


LOGGING_CONFIG = {
    'level': logging.INFO,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%d-%b-%y %H:%M:%S',
    'filename': 'log/log.log',
    'filemode': 'w'
}

DEFAULT_CONFIG_PATH = "config/default.toml"

def two_distance_custom(game: Game, player: PlayerOrder) -> float:
    """Return the difference between the two distances of each player"""
    player_1 = player
    player_2 = PlayerOrder.PLAYER1 if player == PlayerOrder.PLAYER2 else PlayerOrder.PLAYER2
    width, height = game.get_size()
    high_value = width * height
    node_values = {player_1: {}, player_2: {}}
    for player in [player_1, player_2]:
        graph = game.get_graph(player)
        start, end, _, _ = game.get_start_end_order_edge(player)
        distance_start = get_two_distance(game, graph, start, high_value)
        distance_end = get_two_distance(game, graph, end, high_value)
        node_values[player] = {
            node: distance_start[node] + distance_end[node]
            for node in game.get_valid_moves(player_1)
        }
    return player_1, player_2, node_values[player_1], node_values[player_2]

if __name__ == "__main__":
    array = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

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
    
