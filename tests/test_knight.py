import unittest
from src.board import Board
from src.piece import Piece, PieceType


class TestKnight(unittest.TestCase):

    def setUp(self):
        """ Sets up an empty board before each test """
        self.board = Board()
        self.board.place_piece("C1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))

    def test_knight_moves_in_L_shape(self):
        """ A knight should move in an 'L' shape from the center of the board. """
        self.board.place_piece("D4", Piece(PieceType.KNIGHT, Piece.WHITE))
        knight = self.board.get_piece("D4")
        expected_moves = {"B3", "B5", "C2", "C6", "E2", "E6", "F3", "F5"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_knight_jumps_over_pieces(self):
        """ A knight should be able to jump over other pieces. """
        self.board.place_piece("D4", Piece(PieceType.KNIGHT, Piece.WHITE))
        self.board.place_piece("D3", Piece(PieceType.PAWN, Piece.WHITE))  # Blocking piece
        self.board.place_piece("D5", Piece(PieceType.PAWN, Piece.WHITE))  # Blocking piece
        self.board.place_piece("C4", Piece(PieceType.PAWN, Piece.WHITE))  # Blocking piece
        self.board.place_piece("E4", Piece(PieceType.PAWN, Piece.WHITE))  # Blocking piece
        expected_moves = {"B3", "B5", "C2", "C6", "E2", "E6", "F3", "F5"}  # Still valid jumps
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_knight_captures_enemy(self):
        """ A knight should be able to capture an enemy piece. """
        self.board.place_piece("D4", Piece(PieceType.KNIGHT, Piece.WHITE))
        self.board.place_piece("F5", Piece(PieceType.PAWN, Piece.BLACK))  # Enemy piece
        expected_moves = {"B3", "B5", "C2", "C6", "E2", "E6", "F3", "F5"}  # F5 is now a capture move
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_knight_blocked_by_ally(self):
        """ A knight should not be able to move to a square occupied by an allied piece. """
        self.board.place_piece("D4", Piece(PieceType.KNIGHT, Piece.WHITE))
        self.board.place_piece("F5", Piece(PieceType.PAWN, Piece.WHITE))  # Ally piece
        expected_moves = {"B3", "B5", "C2", "C6", "E2", "E6", "F3"}  # F5 is blocked
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_knight_blocked_by_check(self):
        """ A knight defending the king is blocked by a queen """
        self.board.place_piece("C2", Piece(PieceType.KNIGHT, Piece.WHITE))
        self.board.place_piece("C5", Piece(PieceType.QUEEN, Piece.BLACK))
        self.assertEqual(set(self.board.get_valid_moves("C2")), set())


if __name__ == "__main__":
    unittest.main()
