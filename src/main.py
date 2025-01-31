import sys
import os

# add src to sys.path. useful when launching game from chess folder
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.controller import Controller
from src.player_random import RandomPlayer
from src.player_minimax import MinimaxPlayer
from src.piece import Piece

# Run a game simulation
player1 = MinimaxPlayer(Piece.WHITE, 1)
player2 = RandomPlayer(Piece.BLACK)
game = Controller(player1, player2)
game.play_game()
