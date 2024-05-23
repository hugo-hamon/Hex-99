from __future__ import annotations
from ..utils.neighbors import hex_neighbors
from itertools import combinations
import matplotlib.pyplot as plt
from typing import Callable
from ..config import Config
from typing import Optional
from enum import Enum
import networkx as nx
import numpy as np
import time


class PlayerOrder(Enum):
    """Enum for the players"""
    PLAYER1 = 1
    PLAYER2 = 2


MOVE_TYPE = tuple[int, int]


class Game:

    def __init__(self, config: Config, player_controllers: dict[str, Callable]) -> None:
        self.config = config
        self.player_controllers = player_controllers
        self.width, self.height = (
            self.config.game.board_width, self.config.game.board_height
        )

        self.graphs: dict[PlayerOrder, nx.Graph] = {}
        self.over = False
        self.current_player = PlayerOrder.PLAYER1

        self.move_history: list[tuple[nx.Graph, nx.Graph, MOVE_TYPE, PlayerOrder]] = []

    # REQUESTS
    def get_size(self) -> tuple[int, int]:
        """Return the width and height of the board"""
        return self.width, self.height

    def get_graph(self, player: PlayerOrder) -> nx.Graph:
        """Get the graph for the player"""
        return self.graphs[player]

    def get_start_end_order_edge(self, player: PlayerOrder) -> tuple[tuple, tuple, int, int]:
        """Get the start and end nodes of the player"""
        order = 1 if player == PlayerOrder.PLAYER1 else -1
        edge_size = self.width if player == PlayerOrder.PLAYER1 else self.height
        start = (-1, edge_size//2)[::order]
        end = (edge_size, edge_size//2)[::order]
        return start, end, order, edge_size

    def get_opponent(self) -> PlayerOrder:
        """Get the opponent of the current player"""
        return PlayerOrder.PLAYER1 if self.current_player == PlayerOrder.PLAYER2 else PlayerOrder.PLAYER2

    def get_valid_moves(self, player: PlayerOrder) -> list[MOVE_TYPE]:
        """Get the valid moves for the player"""
        graph = self.get_graph(player)
        # -2 to remove the start and end nodes
        return list(graph.nodes)[:-2]

    def get_graph_valid_moves(self, graph: nx.Graph) -> list[MOVE_TYPE]:
        """Get the valid moves for the player"""
        # -2 to remove the start and end nodes
        return list(graph.nodes)[:-2]

    def is_over(self) -> bool:
        """Check if the game is over"""
        return self.over

    def has_won(self, player: PlayerOrder) -> bool:
        """Check if the player has won"""
        graph = self.get_graph(player)
        start, end, _, _ = self.get_start_end_order_edge(player)
        return end in graph.neighbors(start)

    def get_board(self) -> np.ndarray:
        """go through the move history and return the board"""
        board = np.zeros((self.width, self.height))
        for _, _, move, player in self.move_history:
            board[move] = player.value
        return board

    def get_current_player(self) -> PlayerOrder:
        """Get the current player"""
        return self.current_player

    def get_winner(self) -> Optional[PlayerOrder]:
        """Get the winner of the game"""
        if self.over:
            return self.get_current_player()
        return None

    def get_move_history(self) -> list[tuple[nx.Graph, nx.Graph, MOVE_TYPE, PlayerOrder]]:
        """Get the move history"""
        return self.move_history

    # COMMANDS
    def create_board(self) -> None:
        """Create a board of size x size"""
        self.graphs = {
            PlayerOrder.PLAYER1: nx.Graph(),
            PlayerOrder.PLAYER2: nx.Graph()
        }

        # Add neighbors edges
        for player_order in PlayerOrder:
            graph = self.graphs[player_order]
            graph.add_nodes_from(
                [(i, j) for i in range(self.width) for j in range(self.height)]
            )
            for node in graph.nodes:
                neighbors = hex_neighbors(node, self.config)
                neighbors_edges = zip([(node)] * len(neighbors), neighbors)
                graph.add_edges_from(neighbors_edges)

        # Add two nodes, one on each side, to detect if a player has won
        for player_order in PlayerOrder:
            start, end, order, edge_size = self.get_start_end_order_edge(
                player_order
            )
            graph = self.graphs[player_order]
            for i in range(edge_size):
                graph.add_edge(start, (0, i)[::order])
                graph.add_edge(end, (edge_size - 1, i)[::order])

    def move(self, move: MOVE_TYPE, save: bool = True) -> None:
        """Make a move, add to the move history if save is True"""
        graph = self.get_graph(self.current_player)
        opponent_graph = self.get_graph(self.get_opponent())

        if save:
            self.move_history.append((graph.copy(), opponent_graph.copy(), move, self.current_player))
        neighbors = list(graph.neighbors(move))
        for neighbor in combinations(neighbors, 2):
            graph.add_edge(*neighbor)
        graph.remove_node(move)
        opponent_graph.remove_node(move)

        if self.has_won(self.current_player):
            self.over = True
            return

        self.current_player = self.get_opponent()

    def undo(self) -> None:
        """Undo the last move"""
        if not self.move_history or self.is_over():
            return
        graph, opponent_graph, move, player = self.move_history.pop()

        self.current_player = player
        self.graphs[player] = graph
        self.graphs[self.get_opponent()] = opponent_graph

    def update(self) -> None:
        """Update the game state"""
        if self.is_over():
            return
        if len(self.move_history) == self.width * self.height:
            self.over = True
            return
        move = self.player_controllers[self.current_player.name](self)
        if move is None or move not in self.get_valid_moves(self.current_player):
            return
        self.move(move)

    def reset(self) -> None:
        """Reset the game"""
        self.create_board()
        self.move_history = []
        self.over = False
        self.current_player = PlayerOrder.PLAYER1

    def run(self, episodes: int, verbose: bool = False) -> None:
        """Run the game until it is over"""
        winners = {PlayerOrder.PLAYER1: 0, PlayerOrder.PLAYER2: 0}
        for k in range(episodes):
            if verbose:
                print(f"Episode {k+1}/{episodes}")
            while not self.is_over():
                self.update()
            winner = self.get_winner()
            if winner:
                winners[winner] += 1
            self.reset()
        print(f"Player1 wins: {winners[PlayerOrder.PLAYER1]}")
        print(f"Player2 wins: {winners[PlayerOrder.PLAYER2]}")

    def pass_turn(self) -> None:
        """Pass the turn"""
        self.current_player = self.get_opponent()

    # UTILS
    def copy(self) -> Game:
        """Copy the game"""
        new_game = Game(self.config, self.player_controllers)
        new_game.graphs = {
            player: graph.copy() for player, graph in self.graphs.items()
        }
        new_game.current_player = self.current_player
        new_game.move_history = self.move_history.copy()
        new_game.over = self.over
        return new_game

    def draw_graph(self, player: PlayerOrder) -> None:
        """Draw the graph of the player"""
        graph = self.get_graph(player)
        pos = {
            node: np.array([node[0] + 0.5 * node[1], -node[1]])
            for node in graph.nodes
        }
        nx.draw(graph, pos, with_labels=True)
        plt.show()

    def __hash__(self) -> int:
        """Hash the game"""
        return hash(str(self.get_board()))
