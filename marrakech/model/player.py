from dataclasses import dataclass
from random import shuffle

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
        other.money += min(self.money, amount)
        self.money -= min(self.money, amount)


def create_players(count: int) -> list[Player]:
    """Létrehozza a megadott számú játékost

    A játékosok adattagjait a játékosszámtól függően inicializálja.
    """
    if count not in (3, 4):
        raise ValueError("A játékosok száma csak 3 vagy 4 lehet")
    players = list[Player]()
    for i in range(count):
        color = Color(i + 1)
        money = 120 // count
        rugs_left = 15 if count == 3 else 12
        players.append(Player(color, money, rugs_left, f"{color.name} player"))
    shuffle(players)
    return players
