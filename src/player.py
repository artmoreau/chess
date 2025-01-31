from abc import ABC, abstractmethod

from src.board import Board


class Player(ABC):
    """ Abstract class for a chess player. """

    def __init__(self, color: bool):
        self.color = color  # True = White, False = Black

    @abstractmethod
    def choose_move(self, board: Board) -> tuple[str, str]:
        """ Must be implemented by subclasses to choose a move. """
        pass
