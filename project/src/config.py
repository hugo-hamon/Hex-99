from dataclasses import dataclass
from dacite.core import from_dict
import toml


@dataclass
class User:
    player1_algorithm: str
    player2_algorithm: str
    player1_depth: int
    player2_depth: int


@dataclass
class Graphics:
    graphics_enabled: bool


@dataclass
class Game:
    board_width: int
    board_height: int


@dataclass
class Config:
    user: User
    graphics: Graphics
    game: Game


def load_config(config_path: str) -> Config:
    """Load the config"""
    return from_dict(data_class=Config, data=toml.load(config_path))
