from ..game.game import Game, PlayerOrder, MOVE_TYPE
from collections import defaultdict
from enum import Enum
import networkx as nx
import random


class Heuristic(Enum):
    """Enum for the heuristics"""
    # Return a random value between -1 and 1
    RANDOM = "random"
    # Return the difference between the two distances of each player
    TWO_DISTANCE = "two_distance"
    # Use A* to find the shortest path between the two edges
    A_STAR = "a_star"


def evaluate(game: Game, player: PlayerOrder, heuristic: Heuristic) -> float:
    """Return a value for the given game state using the given heuristic"""
    if game.is_over():
        if game.get_winner() == player:
            return 1000
        return -1000

    if heuristic == Heuristic.RANDOM:
        return random_heuristic()
    if heuristic == Heuristic.TWO_DISTANCE:
        return two_distance(game, player)
    if heuristic == Heuristic.A_STAR:
        return a_star(game, player)


def random_heuristic() -> float:
    """Return a random value between -1 and 1"""
    return random.uniform(-1, 1)


def two_distance(game: Game, player: PlayerOrder) -> float:
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
    return min(node_values[player_2].values()) - min(node_values[player_1].values())


def get_two_distance(game: Game, graph: nx.Graph, target: tuple[int, int], high_value: int) -> dict:
    nodes = game.get_graph_valid_moves(graph)
    nodes_values: dict[MOVE_TYPE, int] = defaultdict(lambda: high_value)
    nodes_values[target] = 0

    # Set the values of the border nodes to 1
    for node in graph.neighbors(target):
        nodes_values[node] = 1
        nodes.remove(node)

    # Set nodes with fewer than 2 neighbors to high values
    for node in nodes.copy():
        if len(list(graph.neighbors(node))) < 2:
            # implicit nodes_values[node] = high_value
            nodes.remove(node)
    
    progress = True
    # While new values are being added
    while progress:
        progress = False
        # Create a new buffer for the values
        temp_values = {}
        temp_nodes = nodes.copy()
        for node in nodes:
            sorted_neighbors = sorted(graph.neighbors(node), key=lambda x: nodes_values[x])
            # If the second smallest value is not high_value, set value to equal to it + 1
            if nodes_values[sorted_neighbors[1]] != high_value:
                temp_values[node] = nodes_values[sorted_neighbors[1]] + 1
                progress = True
                temp_nodes.remove(node)
        nodes_values.update(temp_values)
        nodes = temp_nodes

    # For unreachable points, give high values
    for node in nodes:
        nodes_values[node] = high_value
    del nodes_values[target]

    return nodes_values


def a_star(game: Game, player: PlayerOrder) -> float:
    """Return the shortest path between the start and end using the A* algorithm"""
    p1_graph = game.get_graph(PlayerOrder.PLAYER1)
    p2_graph = game.get_graph(PlayerOrder.PLAYER2)
    p1_start, p1_end, _, _ = game.get_start_end_order_edge(PlayerOrder.PLAYER1)
    p2_start, p2_end, _, _ = game.get_start_end_order_edge(PlayerOrder.PLAYER2)

    p1_paths = list(nx.all_shortest_paths(p1_graph, p1_start, p1_end, weight="weight"))
    p2_paths = list(nx.all_shortest_paths(p2_graph, p2_start, p2_end, weight="weight"))

    if player == PlayerOrder.PLAYER1:
        return len(p1_paths) - len(p2_paths)
    return len(p2_paths) - len(p1_paths)
