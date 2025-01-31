import unittest
from src.board import Board
from src.piece import Piece, PieceType


class TestKing(unittest.TestCase):

    def setUp(self):
        """ Sets up an empty board before each test """
        self.board = Board()

    def test_king_moves_one_square_in_all_directions(self):
        """ A king should move one square in any direction. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("D4", Piece(PieceType.KING, Piece.WHITE))
        expected_moves = {"D3", "D5", "C4", "E4", "C3", "C5", "E3", "E5"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_king_blocked_by_ally(self):
        """ A king should be blocked by an allied piece on its path. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("D4", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("D5", Piece(PieceType.PAWN, Piece.WHITE))  # Ally blocking
        expected_moves = {"D3", "C4", "E4", "C3", "C5", "E3", "E5"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_king_can_capture_enemy(self):
        """ A king should be able to capture an enemy piece on its path. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("D4", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("D5", Piece(PieceType.PAWN, Piece.WHITE))  # Enemy piece
        expected_moves = {"D3", "D5", "C4", "E4", "C3", "C5", "E3", "E5"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)


    def test_king_cannot_move_into_check(self):
        """ A king should not be able to move into a check position. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("D4", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("D5", Piece(PieceType.ROOK, Piece.BLACK))  # Rook D5
        self.board.place_piece("G5", Piece(PieceType.KNIGHT, Piece.BLACK))  # Knight G5

        expected_moves = {"C4", "C3", "D5", "E3"}
        self.assertEqual(set(self.board.get_valid_moves("D4")), expected_moves)

    def test_king_little_castling_possible(self):
        """ The king should be able to little castle if conditions are met. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("E1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("H1", Piece(PieceType.ROOK, Piece.WHITE))
        expected_moves = {"D1", "F1", "D2", "E2", "F2", "G1"}  # Castling included
        self.assertEqual(set(self.board.get_valid_moves("E1")), expected_moves)

    def test_king_big_castling_possible(self):
        """ The king should be able to big castle if conditions are met. """
        self.board.place_piece("E1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("E8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("A8", Piece(PieceType.ROOK, Piece.BLACK))
        expected_moves = {"D8", "F8", "D7", "E7", "F7", "C8"}  # Castling included
        self.assertEqual(set(self.board.get_valid_moves("E8")), expected_moves)

    def test_king_castling_blocked(self):
        """ The king should not be able to castle if pieces are blocking the way. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("E1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("H1", Piece(PieceType.ROOK, Piece.WHITE))
        self.board.place_piece("F1", Piece(PieceType.BISHOP, Piece.WHITE))  # Blocking castling
        expected_moves = {"D1", "D2", "E2", "F2"}  # No castling
        self.assertEqual(set(self.board.get_valid_moves("E1")), expected_moves)

    def test_king_castling_through_check(self):
        """ The king should not be able to castle through check. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("E1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("H1", Piece(PieceType.ROOK, Piece.WHITE))
        self.board.place_piece("F8", Piece(PieceType.ROOK, Piece.BLACK))  # Attacking F1
        expected_moves = {"D1", "D2", "E2"}  # No castling
        self.assertEqual(set(self.board.get_valid_moves("E1")), expected_moves)

    def test_king_castling_when_in_check(self):
        """ The king should not be able to castle if it's in check. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("E1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("H1", Piece(PieceType.ROOK, Piece.WHITE))
        self.board.place_piece("E8", Piece(PieceType.ROOK, Piece.BLACK))  # Checking the king
        expected_moves = {"D1", "F1", "D2", "F2"}  # No castling
        self.assertEqual(set(self.board.get_valid_moves("E1")), expected_moves)

    def test_king_castling_not_allowed_if_king_moved(self):
        """ Castling should not be allowed if the king has already moved. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("E2", Piece(PieceType.KING, Piece.WHITE))
        self.board.move_piece('E2', 'E1') # simulate white king move
        self.board.place_piece("H1", Piece(PieceType.ROOK, Piece.WHITE))
        expected_moves = {"D1", "F1", "D2", "E2", "F2"}  # No castling
        self.assertEqual(set(self.board.get_valid_moves("E1")), expected_moves)

    def test_king_castling_not_allowed_if_rook_moved(self):
        """ Castling should not be allowed if the rook has already moved. """
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("E1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("H5", Piece(PieceType.ROOK, Piece.WHITE))
        self.board.move_piece("H5", "H1")
        expected_moves = {"D1", "F1", "D2", "E2", "F2"}  # No castling
        self.assertEqual(set(self.board.get_valid_moves("E1")), expected_moves)

    def test_king_castling_move_the_rook(self):
        """Castling by moving the king must move the rook too. """
        self.board.place_piece("E8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("E1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("A1", Piece(PieceType.ROOK, Piece.WHITE))
        self.board.move_piece("E1", "C1")
        self.assertEqual(self.board.get_piece("D1").kind, PieceType.ROOK)
        self.assertIsNone(self.board.get_piece("A1"))


if __name__ == "__main__":
    unittest.main()
