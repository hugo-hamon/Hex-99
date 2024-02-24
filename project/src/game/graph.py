from __future__ import annotations
from ..utils.neighbors import hex_neighbors
from itertools import combinations
import matplotlib.pyplot as plt
from ..config import Config
import networkx as nx
import numpy as np


class GameGraphManager:
    """Graph representation of the game for both players"""
    def __init__(self, config: Config, allowBacktrack: bool = False) -> None:
        self.allowBacktrack = allowBacktrack
        self.playerGraphs = []
        for i in range(2):
            self.playerGraphs.append(GameGraph(config, i, allowBacktrack))

    def update(self, move: tuple[int,int], player: int) -> None:
        assert player in [0, 1], "player should be 0 or 1"
        self.playerGraphs[player].update(move, True)
        self.playerGraphs[1-player].update(move, False)

    def undo(self) -> None:
        """Undo the last move"""
        assert self.allowBacktrack, "To undo set allowBacktrack to True during instanciation"
        for i in range(2):
            self.playerGraphs[i].undo()
        return
    
    def drawGraph(self, player) -> None:
        """Draw the graph of player in matplotlib"""
        assert player in [0, 1], "player should be 0 or 1"
        self.playerGraphs[player].exportGraph()
        return
    
    def hasWon(self, player) -> None:
        """Return if the player has won"""
        return self.playerGraphs[player].hasWon()
    
    def get_valid_moves(self) -> list[tuple[int, int]]:
        baseMove = self.playerGraphs[0].getNodes()
        return list(self.playerGraphs[0].getNodes())[:-2]


class GameGraph:
    """Graph representation of the game for a player"""
    def __init__(self, config: Config, player: int, allowBacktrack: bool) -> None:
        assert player in [0, 1], "player should be 0 or 1"
        self.size = (config.game.board_width, config.game.board_height)
        self.graph = nx.Graph()
        self.allowBacktrack = allowBacktrack
        if allowBacktrack :
            self.stackGraph = []

        # Add connections
        self.graph.add_nodes_from([(i, j) for i in range(self.size[0]) for j in range(self.size[1])])
        for node in self.graph.nodes:
            neig = hex_neighbors(node, config)
            neigEdges = zip([(node)] * len(neig), neig)
            self.graph.add_edges_from(neigEdges)

        # Add border connections
        edgeSize = self.size[player]
        # If it's the second player then switch the following coordinates backward 
        order = 1 if player == 0 else -1
        self.start = (-1,0)[::order]
        self.end = (edgeSize,0)[::order]
        for i in range(edgeSize):
            self.graph.add_edge(self.start, (0,i)[::order])
            self.graph.add_edge(self.end, (edgeSize-1,i)[::order])
        
    def update(self, move: tuple[int,int], isCurrentPlayer: bool) -> None:
        if self.allowBacktrack:
            self.stackGraph.append(self.graph.copy())
        if isCurrentPlayer:
            neighbors = list(self.graph.neighbors(move))
            for neighbourCouple in combinations(neighbors, 2):
                self.graph.add_edge(*neighbourCouple)    
        self.graph.remove_node(move)
        return

    def drawGraph(self) -> None:
        """draw the graph in matplotlib"""
        d = {node : np.array(node) for node in self.graph.nodes}
        nx.draw(self.graph, pos=d)
        plt.show()
        return

    def undo(self) -> None:
        self.graph = self.stackGraph.pop()
        return
    
    def hasWon(self) -> bool:
        return self.end in self.graph.neighbors(self.start)
    
    def getNodes(self) -> list[tuple[int, int]]:
        return self.graph.nodes