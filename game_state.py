from color import Color
from player import Player, create_players
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class RotationDirection(Enum):
    LEFT = 0
    RIGHT = 1


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

    def intersect(self, other: "RugPos") -> bool:
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


@dataclass
class Rug:
    """Egy szőnyeg adatait leíró osztály"""

    pos: RugPos
    color: Color


class GameState:
    def __init__(self, player_count: int):
        """Inicializálja a játék kezdeti állapotát"""

        self.players = create_players(player_count)
        self._current_player_index = 0

        self.board = [[Color.EMPTY] * 7] * 7
        """7x7 pálya"""

        self.figure_pos = Pos(3, 3)
        self.figure_dir = Direction.UP

        self.top_rugs = set[RugPos]()
        """A teljesen fedetlen szőnyegek pozíciói"""

        self.rugs = list[Rug]()
        """Az összes lerakott szőnyeg (csak a szebb megjelenítés végett)"""

    def current_player(self) -> Player:
        """Visszaadja a jelenlegi játékost"""
        return self.players[self._current_player_index]

    def next_player(self) -> None:
        """Átadja a kört a következő játékosnak"""
        self._current_player_index += 1
        self._current_player_index %= len(self.players)

    def turn_figure(self, direction: RotationDirection) -> None:
        """A figurát 90 fokkal elfordítja a megadott irányba"""
        # TODO

    def move_figure(self, steps: int) -> None:
        """A figurát `steps` lépéssel elmozdítja a jelenlegi irányába

        A figura a pálya szélét elhagyva egy szomszédos sorban folytatja a mozgást.
        Ha a figura egy ellenfél szőnyegén áll meg, az aktuális játékos a régió
        méretével megegyező pénzt fizet a tulajdonosnak.
        """
        # TODO

    def get_region_area(self, pos: Pos) -> int:
        """Visszaadja a megadott pozíciót lefedő szőnyegrégió méretét

        A régió az azonos színű szőnyegek összefüggő területe.
        Ha a megadott mező üres, akkor 0-t ad vissza.
        """
        # TODO
        return 0

    def get_valid_rug_places(self) -> set[RugPos]:
        """Visszaadja az összes olyan helyet, ahova szőnyeget lehet tenni

        A szőnyeg egyik mezőjének szomszédosnak kell lennie a figurával.
        Nem takarhat le teljesen egy fedetlen szőnyeget.
        """
        # TODO
        return set()

    def place_rug(self, pos: RugPos) -> None:
        """Az aktuális játékos lerak egy szőnyeget a megadott helyre"""
        rug = Rug(pos, self.current_player().color)
        self.current_player().rugs_left -= 1
        self.rugs.append(rug)
        # TODO: frissíteni a `board` állapotát
        # TODO: törölni a `top_rugs` lefedésre került szőnyegeit
        self.top_rugs.add(pos)

    def is_game_over(self) -> bool:
        """Megadja, hogy vége van-e a játéknak

        A játék akkor ér véget, ha minden játékosnak elfogytak a szőnyegei."""
        # TODO
        return False
