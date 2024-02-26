from src.game.graph import GameGraphManager
from src.config import load_config

if __name__ == "__main__":
    path = "config/default.toml"
    config = load_config(path)
    G = GameGraphManager(config, True)
    G.update((0,0), 0)
    G.update((2, 1), 0)
    G.update((2, 2), 0)
    print(G.get_valid_moves())