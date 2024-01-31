from dataclasses import dataclass
from dacite.core import from_dict
import toml
"""
[user]
player1_algorithm = "human"
player2_algorithm = "human"

[graphics]
graphics_enabled = true
width = 1080
height = 720
title = "Hex - Pierre Praden & Hugo Hamon"

[game]
board_width = 11
board_height = 11
"""


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


@dataclass
class Config:
    user: User
    graphics: Graphics
    game: Game


def load_config(config_path: str) -> Config:
    """Load the config"""
    return from_dict(data_class=Config, data=toml.load(config_path))
