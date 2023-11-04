from dataclasses import dataclass

from .color import Color


@dataclass
class Player:
    color: Color
    money: int
    rugs_left: int
    name: str = ""

    def pay_to(self, other: "Player", amount: int) -> None:
        """Pénz fizetése egy másik játékosnak

        Ha nincs elég pénze, akkor annyit fizet, amennyit tud.
        """
        # TODO


def create_players(count: int) -> list[Player]:
    """Létrehozza a megadott számú játékost

    A játékosok adattagjait a játékosszámtól függően inicializálja.
    """
    # TODO
    return []
