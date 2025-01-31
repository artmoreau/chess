from __future__ import annotations
from enum import Enum


class PieceType(Enum):
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


class Piece:

    WHITE = True
    BLACK = False

    SYMBOLS_LOG = {
        PieceType.PAWN:   ("♙", "♟"),
        PieceType.KNIGHT: ("♘", "♞"),
        PieceType.BISHOP: ("♗", "♝"),
        PieceType.ROOK:   ("♖", "♜"),
        PieceType.QUEEN:  ("♕", "♛"),
        PieceType.KING:   ("♔", "♚"),
    }

    SYMBOLS = {
        PieceType.PAWN: ("P", "p"),
        PieceType.KNIGHT: ("N", "n"),
        PieceType.BISHOP: ("B", "b"),
        PieceType.ROOK: ("R", "r"),
        PieceType.QUEEN: ("Q", "q"),
        PieceType.KING: ("K", "k"),
    }

    piece_values = {
        PieceType.PAWN: 1,
        PieceType.KNIGHT: 3,
        PieceType.BISHOP: 3,
        PieceType.ROOK: 5,
        PieceType.QUEEN: 9,
        PieceType.KING: 1000
    }

    def __init__(self, kind: PieceType, color: bool):
        if not isinstance(kind, PieceType):
            raise ValueError("kind must be a PieceType enum value")
        self._kind = kind
        self._color = color
        self._has_moved = False  # Track if the piece has moved
        self._score = self.piece_values[kind] * 1 if color == Piece.WHITE else -1  # positive score for white

    @property
    def kind(self) -> PieceType:
        return self._kind

    @property
    def color(self) -> bool:
        return self._color

    @property
    def has_moved(self) -> bool:
        return self._has_moved

    @property
    def score(self) -> int:
        return self._score

    def mark_as_moved(self):
        """Marks the piece as having moved."""
        self._has_moved = True

    def unmark_as_moved(self):
        """Marks the piece as having moved."""
        self._has_moved = False

    def __str__(self) -> str:
        color_str = "white" if self.color == self.WHITE else "black"
        return f"{self.kind.value} {color_str}"

    def symbol_log(self) -> str:
        """return Unicode symbol for piece. used for log console"""
        return self.SYMBOLS_LOG[self.kind][0 if self.color == self.WHITE else 1]

    def symbol(self) -> str:
        """return lettre symbole for piece. used for pygame to draw"""
        return self.SYMBOLS[self.kind][0 if self.color == self.WHITE else 1]
