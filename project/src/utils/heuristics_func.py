from ..game.game import Game, PlayerOrder, MOVE_TYPE
from collections import defaultdict
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from typing import Optional


class Heuristic(Enum):
    """Enum for the heuristics"""
    RANDOM = "random"  # Return a random value between -1 and 1
    # Return the difference between the two distances of each player
    TWO_DISTANCE = "two_distance"


def evaluate(game: Game, player: PlayerOrder, heuristic: Heuristic) -> float:
    """Return a value for the given game state using the given heuristic"""
    if game.is_over():
        if game.get_winner() == player:
            return float('inf')
        return float('-inf')

    if heuristic == Heuristic.RANDOM:
        return random_heuristic()
    if heuristic == Heuristic.TWO_DISTANCE:
        return two_distance(game, player)
    return 0


def random_heuristic() -> float:
    """Return a random value between -1 and 1"""
    return random.uniform(-1, 1)


def two_distance(game: Game, player: PlayerOrder) -> float:
    """Return the difference between the two distances of each player"""
    player_1 = game.get_current_player()
    player_2 = game.get_opponent()
    p1_graph = game.get_graph(player_1)
    p2_graph = game.get_graph(player_2)
    p1_start, p1_end, _, _ = game.get_start_end_order_edge(player_1)
    p2_start, p2_end, _, _ = game.get_start_end_order_edge(player_2)
    width, height = game.get_size()
    high_value = width * height

    distance_p1_start = get_two_distance(game, p1_graph, p1_start, high_value)
    distance_p1_end = get_two_distance(game, p1_graph, p1_end, high_value)
    distance_p2_start = get_two_distance(game, p2_graph, p2_start, high_value)
    distance_p2_end = get_two_distance(game, p2_graph, p2_end, high_value)
    node_values = {
        node: distance_p1_start[node] + distance_p1_end[node] -
        distance_p2_start[node] - distance_p2_end[node]
        for node in game.get_valid_moves(player_1)
    }
    return min(node_values.values())


def get_two_distance(game: Game, graph: nx.Graph, target: tuple[int, int], high_value: int) -> dict:
    nodes = game.get_graph_valid_moves(graph)
    nodes_values: dict[MOVE_TYPE, Optional[int]] = {
        node: None for node in nodes
    }
    nodes_values[target] = 0
    progress = True
    while progress:
        progress = False
        temp_values = {}
        temp_nodes = nodes.copy()
        for node in nodes:
            second_delay = False
            for neighbor in sorted(graph.neighbors(node), key=lambda x: (nodes_values[x] if x in nodes_values.keys() and nodes_values[x] != None else high_value,)):
                if neighbor == target:
                    progress = True
                    temp_values[node] = 1
                    temp_nodes.remove(node)
                    break
                if neighbor not in nodes_values.keys():
                    continue
                node_value = nodes_values[neighbor]
                if node_value is not None:
                    if second_delay == True:
                        progress = True
                        temp_values[node] = node_value + 1
                        temp_nodes.remove(node)
                        break
                    second_delay = True
        nodes_values.update(temp_values)
        nodes = temp_nodes
    # For unreachable points, give high values
    for node in nodes:
        nodes_values[node] = high_value
    del nodes_values[target]
    return nodes_values
