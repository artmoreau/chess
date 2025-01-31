import random
from typing import Optional

from src.board import Board
from src.player import Player

class RandomPlayer(Player):
    """ A basic chess player that selects moves randomly. """

    def choose_move(self, board: Board) -> Optional[tuple[str, str]]:
        """ Selects a random valid move from the available moves. """
        valid_moves = board.get_valid_moves_for_color(self.color)
        return random.choice(valid_moves) if valid_moves else None # Select a random move
