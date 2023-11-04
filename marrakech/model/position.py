from dataclasses import dataclass


@dataclass
class Pos:
    """A pálya egy mezőjének koordinátái

    A bal felső sarok koordinátái (0, 0)
    """

    row: int
    col: int

    def as_tuple(self) -> tuple[int, int]:
        return (self.row, self.col)

    def distance(self, other: "Pos") -> int:
        """Megadja a két mező Manhattan-távolságát"""
        return abs(self.row - other.row) + abs(self.col - other.col)

    def neighbors(self) -> list["Pos"]:
        """Megadja a mező érvényes szomszédait a 7x7-es pályán"""
        raise NotImplementedError
        return []
