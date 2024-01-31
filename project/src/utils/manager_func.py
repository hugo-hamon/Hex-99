from ..manager.random_manager import RandomManager
from ..manager.user_manager import UserManager
from ..manager.manager import Manager
from ..config import Config
import logging
import sys


def match_manager(config: Config, manager_name: str) -> Manager:
    """Return a manager from the config"""
    match manager_name:
        case "human":
            return UserManager()
        case "random":
            return RandomManager()
        case _:
            logging.error(
                f'Found "{manager_name}" in class App in method match_manager'
            )
            sys.exit(1)