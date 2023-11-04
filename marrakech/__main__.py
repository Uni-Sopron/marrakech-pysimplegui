"""A játékprogram belépési pontja."""

from .model.game_state import GameState
from .gui.mainwindow import MainWindow

game = GameState(4)
window = MainWindow(game)
window.start()
