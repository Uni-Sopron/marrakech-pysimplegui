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
        neighbors = [
            Pos(self.row - 1, self.col),
            Pos(self.row + 1, self.col),
            Pos(self.row, self.col - 1),
            Pos(self.row, self.col + 1),
        ]
        neighbors = [n for n in neighbors if 0 <= n.row < 7 and 0 <= n.col < 7]
        return neighbors
