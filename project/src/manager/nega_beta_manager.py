from ..utils.heuristics_func import Heuristic, evaluate
from ..game.game import Game, PlayerOrder
from .manager import Manager
from ..config import Config
from typing import Optional


class NegaBetaManager(Manager):

    def __init__(self, config: Config, depth: int) -> None:
        super().__init__(config)
        self.depth = depth
        self.transposition_table = {}
        if depth < 1:
            raise ValueError("NegaBeta depth should be at least 1")

    def reset(self) -> None:
        """Reset the manager"""
        pass

    def check_for_winning_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Check if there is a winning move in the current game state"""
        for move in game.get_valid_moves(game.get_current_player()):
            game_copy = game.copy()
            game_copy.move(move)
            if game_copy.is_over():
                return move
        return None

    def get_move(self, game: Game) -> Optional[tuple[int, int]]:
        """Return the best move using the alpha beta algorithm"""
        return self.negabeta_transposition(
            game, self.depth, float('-inf'), float('inf'),
            1, game.get_current_player()
        )[1]
        # return self.negabeta(
        #     game, self.depth, float('-inf'), float('inf'),
        #     1, game.get_current_player()
        # )[1]

    def negabeta(self, game: Game, depth: int, alpha: float, beta: float, color: int, player: PlayerOrder) -> tuple[float, Optional[tuple[int, int]]]:
        """Nega-beta pruning algorithm"""
        if depth == 0 or game.is_over():
            return color * evaluate(game, player, Heuristic.A_STAR), None
        
        best_move = None
        value = float('-inf')
        for move in game.get_valid_moves(game.get_current_player()):
            game_copy = game.copy()
            game_copy.move(move)
            move_value, _ = self.negabeta(
                game_copy, depth - 1, -beta, -alpha, -color, player
            )
            move_value = -move_value
            if move_value > value:
                value = move_value
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return value, best_move
    
    def negabeta_transposition(self, game: Game, depth: int, alpha: float, beta: float, color: int, player: PlayerOrder) -> tuple[float, Optional[tuple[int, int]]]:
        """Nega-beta pruning algorithm with transposition table"""
        alpha_original = alpha

        tt_entry = self.transposition_table.get(hash(game))
        if tt_entry and tt_entry["depth"] >= depth:
            if tt_entry["flag"] == "EXACT":
                return tt_entry["value"], tt_entry["move"]
            elif tt_entry["flag"] == "LOWERBOUND":
                alpha = max(alpha, tt_entry["value"])
            elif tt_entry["flag"] == "UPPERBOUND":
                beta = min(beta, tt_entry["value"])
            if alpha >= beta:
                return tt_entry["value"], tt_entry["move"]
            
        if depth == 0 or game.is_over():
            return color * evaluate(game, player, Heuristic.A_STAR), None
        
        best_move = None
        value = float('-inf')
        for move in game.get_valid_moves(game.get_current_player()):
            game_copy = game.copy()
            game_copy.move(move)
            move_value, _ = self.negabeta_transposition(
                game_copy, depth - 1, -beta, -alpha, -color, player
            )
            move_value = -move_value
            if move_value > value:
                value = move_value
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        if tt_entry is None:
            tt_entry = {}

        tt_entry["value"] = value
        if value <= alpha_original:
            tt_entry["flag"] = "UPPERBOUND"
        elif value >= beta:
            tt_entry["flag"] = "LOWERBOUND"
        else:
            tt_entry["flag"] = "EXACT"
        tt_entry["move"] = best_move
        tt_entry["depth"] = depth
        self.transposition_table[hash(game)] = tt_entry

        return value, best_move

