"""A szőnyegek adatait, valamint pozíciókat és irányokat leíró segédosztályok"""

from dataclasses import dataclass
from enum import Enum

from color import Color


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


@dataclass
class RugPos:
    """Egy szőnyeg pozícióját leíró osztály

    A `start` megadja az egyik felének a koordinátáit, a `direction` pedig azt, hogy a
    szőnyeg másik fele ettől milyen irányban van.
    """

    start: Pos
    direction: Direction

    def intersects(self, other: "RugPos") -> bool:
        """Megadja, hogy fedésben van-e egymással a két szőnyeg"""
        # TODO
        return False

    def as_tuple(self) -> tuple[Pos, Pos]:
        """Visszaadja a szőnyeg két mezőjének koordinátáit"""
        # TODO
        return (self.start, Pos(0, 0))

    @staticmethod
    def from_tuple(positions: tuple[Pos, Pos]) -> "RugPos":
        """Létrehoz egy `RugPos` objektumot a két mező koordinátáiból"""
        # TODO
        return RugPos(positions[0], Direction.UP)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RugPos):
            return False
        tup1 = self.as_tuple()
        tup2 = other.as_tuple()
        if tup1 == tup2:
            return True
        if tup1 == (tup2[1], tup2[0]):
            return True
        return False


@dataclass
class Rug:
    """Egy szőnyeg adatait leíró osztály"""

    pos: RugPos
    color: Color
