import unittest
from src.board import Board
from src.piece import Piece, PieceType


class TestQueen(unittest.TestCase):

    def setUp(self):
        """ Sets up an empty board before each test """
        self.board = Board()
        self.board.place_piece("C1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))

    def test_queen_moves_vertically_horizontally_and_diagonally(self):
        """ A queen should move vertically, horizontally, and diagonally. """
        self.board.place_piece("D4", Piece(PieceType.QUEEN, Piece.WHITE))
        expected_moves = {"D1", "D2", "D3", "D5", "D6", "D7", "D8", "A4", "B4", "C4", "E4", "F4", "G4", "H4",
                          "C3", "B2", "A1", "E5", "F6", "G7", "H8", "C5", "B6", "A7", "E3", "F2", "G1"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_queen_blocked_by_ally(self):
        """ A queen should be blocked by an allied piece on its path. """
        self.board.place_piece("D4", Piece(PieceType.QUEEN, Piece.WHITE))
        self.board.place_piece("D5", Piece(PieceType.PAWN, Piece.WHITE))  # Ally blocking
        expected_moves = {"D1", "D2", "D3", "A4", "B4", "C4", "E4", "F4", "G4", "H4",
                          "C3", "B2", "A1", "E5", "F6", "G7", "H8", "C5", "B6", "A7", "E3", "F2", "G1"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_queen_can_capture_enemy_diagonally(self):
        """ A queen should be able to capture an enemy piece on its diagonally path. """
        self.board.place_piece("D4", Piece(PieceType.QUEEN, Piece.WHITE))
        self.board.place_piece("D6", Piece(PieceType.PAWN, Piece.BLACK))  # Enemy piece
        expected_moves = {"D1", "D2", "D3", "D5", "D6", "A4", "B4", "C4", "E4", "F4", "G4", "H4",
                          "C3", "B2", "A1", "E5", "F6", "G7", "H8", "C5", "B6", "A7", "E3", "F2", "G1"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_queen_can_capture_enemy_horizontally(self):
        """ A queen should be able to capture an enemy piece on its horizontally path. """
        self.board.place_piece("D4", Piece(PieceType.QUEEN, Piece.WHITE))
        self.board.place_piece("F4", Piece(PieceType.PAWN, Piece.BLACK))  # Enemy piece
        expected_moves = {"D1", "D2", "D3", "D5", "D6", "D7", "D8", "A4", "B4", "C4", "E4", "F4",
                          "C3", "B2", "A1", "E5", "F6", "G7", "H8", "C5", "B6", "A7", "E3", "F2", "G1"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_queen_blocked_by_check(self):
        """ A queen defending the king is vertically blocked by a rook """
        self.board.place_piece("C2", Piece(PieceType.QUEEN, Piece.WHITE))
        self.board.place_piece("C5", Piece(PieceType.ROOK, Piece.BLACK))
        expected_moves = {"C3", "C4", "C5"}
        self.assertEqual(set(self.board.get_valid_moves("C2")), expected_moves)


if __name__ == "__main__":
    unittest.main()
