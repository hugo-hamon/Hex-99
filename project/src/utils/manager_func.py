from ..manager.alpha_beta_manager import AlphaBetaManager
from ..manager.nega_beta_manager import NegaBetaManager
from ..manager.minimax_manager import MinimaxManager
from ..manager.random_manager import RandomManager
from ..manager.user_manager import UserManager
from ..manager.sss_manager import SSSManager
from ..manager.manager import Manager
from ..config import Config
import logging
import sys


def match_manager(config: Config, manager_name: str, depth: int) -> Manager:
    """Return a manager from the config"""
    match manager_name:
        case "human":
            return UserManager(config)
        case "random":
            return RandomManager(config)
        case "minimax":
            return MinimaxManager(config, depth)
        case "alpha_beta":
            return AlphaBetaManager(config, depth)
        case "nega_beta":
            return NegaBetaManager(config, depth)
        case "sss":
            return SSSManager(config, depth)
        case _:
            logging.error(
                f'Found "{manager_name}" in class App in method match_manager'
            )
            sys.exit(1)
