from src.game.graph import GameGraphManager
from src.config import load_config
from src.utils.heuristics_func import *

if __name__ == "__main__":
    path = "config/default.toml"
    config = load_config(path)
    G = GameGraphManager(config, True)
    two_distance(G)
    

