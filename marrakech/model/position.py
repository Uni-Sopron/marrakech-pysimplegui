from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    """A pálya egy mezőjének koordinátái

    A bal felső sarok koordinátái (0, 0)
    """

    row: int
    col: int
