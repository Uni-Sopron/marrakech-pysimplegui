from marrakech.model.color import Color
from .board import Board
from .directions import Direction, RotationDirection
from .player import Player, create_players
from .position import Pos
from .rug import Rug, RugPos


class GameState:
    """A játék aktuális állapotát leíró osztály"""

    def __init__(self, player_count: int) -> None:
        """Inicializálja a játék kezdeti állapotát"""

        self.players = create_players(player_count)
        self._current_player_index = 0

        self.board = Board()

        self.figure_pos = Pos(3, 3)
        self.figure_dir = Direction.UP

        self.top_rugs = list[RugPos]()
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
        self.figure_dir = self.figure_dir.rotate(direction)

    def step_with_figure(self) -> None:
        """A figura egy mezőt lép a jelenlegi irányába

        Ha a figura lelépne a pályáról, az erkélyt követve visszatér a pályára egy
        szomszédos sorba, vagy a fordító saroknál a kiindulási mezőre, elfordulva.
        """
        if self.figure_dir == Direction.UP:
            self.figure_pos.row -= 1
        elif self.figure_dir == Direction.DOWN:
            self.figure_pos.row += 1
        elif self.figure_dir == Direction.LEFT:
            self.figure_pos.col -= 1
        elif self.figure_dir == Direction.RIGHT:
            self.figure_pos.col += 1
        if self.figure_pos.row < 0:
            # fenti erkély
            self.figure_pos.row = 0
            if self.figure_pos.col == 6:
                self.figure_dir = Direction.LEFT
            else:
                self.figure_dir = Direction.DOWN
                self.figure_pos.col += 1 if self.figure_pos.col % 2 == 0 else -1
        elif self.figure_pos.row > 6:
            # alsó erkély
            self.figure_pos.row = 6
            if self.figure_pos.col == 0:
                self.figure_dir = Direction.RIGHT
            else:
                self.figure_dir = Direction.UP
                self.figure_pos.col += 1 if self.figure_pos.col % 2 == 1 else -1
        elif self.figure_pos.col < 0:
            # baloldali erkély
            self.figure_pos.col = 0
            if self.figure_pos.row == 6:
                self.figure_dir = Direction.UP
            else:
                self.figure_dir = Direction.RIGHT
                self.figure_pos.row += 1 if self.figure_pos.row % 2 == 0 else -1
        elif self.figure_pos.col > 6:
            # jobboldali erkély
            self.figure_pos.col = 6
            if self.figure_pos.row == 0:
                self.figure_dir = Direction.DOWN
            else:
                self.figure_dir = Direction.LEFT
                self.figure_pos.row += 1 if self.figure_pos.row % 2 == 1 else -1

    def move_figure(self, steps: int) -> None:
        """A figura `steps` lépést tesz a jelenlegi irányába

        Ha a figura egy ellenfél szőnyegén áll meg, az aktuális játékos a régió
        méretével megegyező pénzt fizet a tulajdonosnak.
        """
        for _ in range(steps):
            self.step_with_figure()
        if self.board.get(self.figure_pos) != Color.EMPTY:
            for player in self.players:
                if player.color == self.board.get(self.figure_pos):
                    area = self.board.get_region_area(self.figure_pos)
                    self.current_player().pay_to(player, area)
                    break

    def get_valid_rug_places(self) -> list[RugPos]:
        """Visszaadja az összes olyan helyet, ahova szőnyeget lehet tenni

        A szőnyeg egyik mezőjének szomszédosnak kell lennie a figurával.
        Nem takarhat le teljesen egy fedetlen szőnyeget.
        """
        places = list[RugPos]()
        for start in self.figure_pos.neighbors():
            for end in start.neighbors():
                if end == self.figure_pos:
                    continue
                pos = RugPos.from_tuple((start, end))
                for top in self.top_rugs:
                    if pos == top:
                        break
                else:
                    places.append(pos)
        return places

    def place_rug(self, pos: RugPos) -> None:
        """Az aktuális játékos lerak egy szőnyeget a megadott helyre"""
        rug = Rug(pos, self.current_player().color)
        self.current_player().rugs_left -= 1
        self.rugs.append(rug)
        self.board.place_rug(rug)
        # törölni kell a `top_rugs` lefedésre került szőnyegeit
        self.top_rugs = [r for r in self.top_rugs if not r.intersects(pos)]
        self.top_rugs.append(pos)

    def is_game_over(self) -> bool:
        """Megadja, hogy vége van-e a játéknak

        A játék akkor ér véget, ha minden játékosnak elfogytak a szőnyegei."""
        return all(player.rugs_left == 0 for player in self.players)

    def get_scoreboard(self) -> list[tuple[str, int]]:
        """Visszaadja a játékosok neveit és pontszámait helyezés szerinti sorrendben

        A pontszám a pénz és a fedetlen szőnyegfelület összege.
        Pontegyezés esetén a nagyobb szőnyegfelület számít jobb eredménynek.
        """
        areas = {player.name: 0 for player in self.players}
        for row in self.board.fields:
            for player in self.players:
                areas[player.name] += row.count(player.color)
        scores = [
            (player.name, player.money + areas[player.name]) for player in self.players
        ]

        def key(item):
            player_name, score = item
            return score, areas[player_name]

        scores.sort(key=key, reverse=True)
        return scores
