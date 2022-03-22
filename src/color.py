from enum import IntEnum, auto


class Color(IntEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    BLACK = auto()
    PURPLE = auto()
    YELLOW = auto()


COLORS = set(Color)

aliases = {
    "R": "RED",
    "G": "GREEN",
    "BL": "BLUE",
    "B": "BLACK",
    "P": "PURPLE",
    "Y": "YELLOW",
}
