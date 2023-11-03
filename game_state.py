from color import Color
from player import Player, create_players
from rug import Direction, Pos, RotationDirection, Rug, RugPos


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
        if direction == RotationDirection.NONE:
            return
        # TODO

    def step_with_figure(self) -> None:
        """A figura egy mezőt lép a jelenlegi irányába

        A figura a pálya szélét elhagyva egy szomszédos sorban folytatja a mozgást.
        """
        # TODO

    def move_figure(self, steps: int) -> None:
        """A figura `steps` lépést tesz a jelenlegi irányába

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

    def get_scoreboard(self) -> list[tuple[Player, int]]:
        """Visszaadja a játékosokat és pontszámaikat helyezés szerinti sorrendben

        A pontszám a pénz és a fedetlen szőnyegfelület összege.
        Pontegyezés esetén a nagyobb szőnyegfelület számít jobb eredménynek.
        """
        # TODO
        return []
