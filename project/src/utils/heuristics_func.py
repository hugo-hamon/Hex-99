from ..game.graph import GameGraphManager, GameGraph
from ..game.game import Game, PlayerOrder
from collections import defaultdict
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random


class Heuristic(Enum):
    """Enum for the heuristics"""
    RANDOM = "random"  # Return a random value between -1 and 1
    TWO_DISTANCE = "two_distance"  # Return the difference between the two distances of each player


def evaluate(game: Game, player: PlayerOrder, heuristic: Heuristic) -> float:
    """Return a value for the given game state using the given heuristic"""
    if game.is_over():
        if game.get_winner() == player:
            return float('inf')
        return float('-inf')

    if heuristic == Heuristic.RANDOM:
        return random_heuristic()
    if heuristic == Heuristic.TWO_DISTANCE:
        return two_distance(game.get_game_graphs())
    return 0.0


def random_heuristic() -> float:
    """Return a random value between -1 and 1"""
    return random.uniform(-1, 1)

def two_distance(graph: GameGraphManager) -> float:
    """Return the difference between the two distances of each player"""
    

    
    gameGraph0, gameGraph1 = graph.get_game_graphs()
    start0 = gameGraph0.start
    start1 = gameGraph1.start
    end0 = gameGraph0.end
    end1 = gameGraph1.end
    graph0 = gameGraph0.graph
    graph1 = gameGraph1.graph
    highValue = gameGraph0.size[0] * gameGraph0.size[1]
    d0s = get_two_distance(graph0, start0, highValue)
    d0e = get_two_distance(graph0, end0, highValue)
    d1s = get_two_distance(graph1, start1, highValue)
    d1e = get_two_distance(graph1, end1, highValue)
    values = {node: d0s[node] + d0e[node] - d1s[node] - d1e[node] for node in list(graph0.nodes)[:-2]}
    return min(values.values()) 
    

def get_two_distance(graph: nx.graph, target: tuple[int,int], highValue: float) -> float:
    nodes = list(graph.nodes)[:-2]
    nodesValues = {node: None for node in nodes}
    nodesValues[target] = 0
    progress = True
    while progress:
        progress = False
        for node in nodes:
            secondDelay = False
            for neighbor in sorted(graph.neighbors(node), key=lambda x: nodesValues[x] if x in nodesValues.keys() and nodesValues[x] != None else highValue):
                if neighbor == target:
                    progress = True
                    nodesValues[node] = 1
                    nodes.remove(node)
                    break
                if neighbor not in nodesValues.keys():
                    continue
                if nodesValues[neighbor] is not None:
                    if secondDelay == True:
                        progress = True
                        nodesValues[node] = nodesValues[neighbor] + 1
                        nodes.remove(node)
                        break
                    secondDelay = True
    # For unreachable points, give high values
    for node in nodes:
        nodesValues[node] = highValue
    del nodesValues[target]
    return nodesValues
        
                
    

