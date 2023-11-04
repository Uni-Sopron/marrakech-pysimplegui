from dataclasses import dataclass

from .color import Color
from .directions import Direction
from .position import Pos


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
        return set(self.as_tuple()).intersection(set(other.as_tuple())) != set()

    def as_tuple(self) -> tuple[Pos, Pos]:
        """Visszaadja a szőnyeg két mezőjének koordinátáit"""
        if self.direction == Direction.UP:
            return (self.start, Pos(self.start.row - 1, self.start.col))
        if self.direction == Direction.DOWN:
            return (self.start, Pos(self.start.row + 1, self.start.col))
        if self.direction == Direction.LEFT:
            return (self.start, Pos(self.start.row, self.start.col - 1))
        if self.direction == Direction.RIGHT:
            return (self.start, Pos(self.start.row, self.start.col + 1))
        raise ValueError("Ismeretlen irány.")

    @staticmethod
    def from_tuple(positions: tuple[Pos, Pos]) -> "RugPos":
        """Létrehoz egy `RugPos` objektumot a két mező koordinátáiból

        Ha a két mező nem szomszédos, akkor `ValueError` kivételt dob.
        """
        if positions[0].distance(positions[1]) != 1:
            raise ValueError("A két mező nem szomszédos.")
        start, end = positions
        if start.row == end.row:
            if start.col < end.col:
                return RugPos(start, Direction.RIGHT)
            else:
                return RugPos(start, Direction.LEFT)
        else:
            if start.row < end.row:
                return RugPos(start, Direction.DOWN)
            else:
                return RugPos(start, Direction.UP)

    def __eq__(self, other: object) -> bool:
        """Két `RugPos` objektum akkor egyenlő, ha teljesen fedik egymást"""
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
