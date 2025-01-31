import unittest

from src.board import Board
from src.piece import Piece, PieceType


class TestBishop(unittest.TestCase):

    def setUp(self):
        """ Sets up an empty board before each test """
        self.board = Board()
        self.board.place_piece("C1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))

    def test_bishop_moves_freely_diagonally(self):
        """ A bishop should be able to move freely in diagonal directions. """
        self.board.place_piece("D4", Piece(PieceType.BISHOP, Piece.WHITE))
        expected_moves = {"C3", "B2", "A1", "E5", "F6", "G7", "H8", "C5", "B6", "A7", "E3", "F2", "G1"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_bishop_blocked_by_ally(self):
        """ A bishop should be blocked by an allied piece on its path. """
        self.board.place_piece("D4", Piece(PieceType.BISHOP, Piece.WHITE))
        self.board.place_piece("E5", Piece(PieceType.PAWN, Piece.WHITE))  # Ally blocking
        expected_moves = {"C3", "B2", "A1", "C5", "B6", "A7", "E3", "F2", "G1"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_bishop_can_capture_enemy(self):
        """ A bishop should be able to capture an enemy piece on its path. """
        self.board.place_piece("D4", Piece(PieceType.BISHOP, Piece.WHITE))
        self.board.place_piece("F6", Piece(PieceType.PAWN, Piece.BLACK))  # Enemy piece
        expected_moves = {"C3", "B2", "A1", "E5", "F6", "C5", "B6", "A7", "E3", "F2", "G1"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_bishop_blocked_by_check(self):
        """ A bishop defending the king is blocked by a queen """
        self.board.place_piece("C2", Piece(PieceType.BISHOP, Piece.WHITE))
        self.board.place_piece("C5", Piece(PieceType.QUEEN, Piece.BLACK))
        self.assertEqual(set(self.board.get_valid_moves("C2")), set())


if __name__ == "__main__":
    unittest.main()
