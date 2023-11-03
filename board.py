from dataclasses import dataclass
from enum import Enum

from color import Color
from rug import Rug


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class RotationDirection(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2


@dataclass
class Pos:
    """A pálya egy mezőjének koordinátái

    A bal felső sarok koordinátái (0, 0)
    """

    row: int
    col: int


class Board:
    def __init__(self) -> None:
        self.fields = [[Color.EMPTY] * 7] * 7
        """7x7 pálya, kezdetben teljesen üres"""

    def get(self, pos: Pos) -> Color:
        return self.fields[pos.row][pos.col]

    def _set(self, pos: Pos, color: Color) -> None:
        self.fields[pos.row][pos.col] = color

    def place_rug(self, rug: Rug) -> None:
        for pos in rug.pos.as_tuple():
            self._set(pos, rug.color)

    def get_region_area(self, pos: Pos) -> int:
        """Visszaadja a megadott pozíciót lefedő szőnyegrégió méretét

        A régió az azonos színű szőnyegek összefüggő területe.
        Ha a megadott mező üres, akkor 0-t ad vissza.
        """
        # TODO
        return 0
