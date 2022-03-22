from enum import Enum

class Color(Enum):
    RED: Color
    GREEN: Color
    BLUE: Color
    BLACK: Color
    PURPLE: Color
    YELLOW: Color

COLORS: set[Color]

aliases: dict[str, str]
