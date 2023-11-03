from ..model.directions import Direction, RotationDirection
from ..model.game_state import GameState
from ..model.player import Player
from ..model.position import Pos
from ..model.rug import RugPos


class Agent:
    """MI játékost megvalósító osztály"""

    def __init__(self, player: Player, game_state: GameState) -> None:
        """Eltárolja a játékos adataira és a játék állapotára mutató referenciákat"""
        self.player = player
        self.game_state = game_state

    def decide_rotation(self) -> RotationDirection:
        """Eldönti, hogy a figura melyik irányba forduljon"""
        # TODO
        return RotationDirection.NONE

    def decide_rug_placement(self) -> RugPos:
        """Eldönti, hogy hova rakja le a szőnyeget"""
        # TODO
        return RugPos(Pos(0, 0), Direction.UP)