from dataclasses import dataclass
from dacite.core import from_dict
import toml


@dataclass
class Minimax:
    depth: int


@dataclass
class User:
    player1_algorithm: str
    player2_algorithm: str


@dataclass
class Graphics:
    graphics_enabled: bool


@dataclass
class Game:
    board_width: int
    board_height: int
    allow_backtrack: bool

@dataclass
class Config:
    user: User
    graphics: Graphics
    game: Game
    minimax: Minimax


def load_config(config_path: str) -> Config:
    """Load the config"""
    return from_dict(data_class=Config, data=toml.load(config_path))
