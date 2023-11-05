"""A játékprogram belépési pontja."""

from .model.game_state import GameState

print("Setting up for 3 players...")
game = GameState(3)
print(game.board)
