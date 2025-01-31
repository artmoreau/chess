import unittest
from src.board import Board
from src.piece import Piece, PieceType


class TestPawn(unittest.TestCase):

    def setUp(self):
        """ Sets up an empty board before each test """
        self.board = Board()
        self.board.place_piece("C1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("C8", Piece(PieceType.KING, Piece.BLACK))

    def test_pawn_moves_one_step(self):
        """ A pawn should move one step forward if the square is empty. """
        self.board.place_piece("D4", Piece(PieceType.PAWN, Piece.WHITE))
        self.assertEqual(set(self.board.get_valid_moves("D4")), {"D5"})

    def test_pawn_moves_two_steps(self):
        """ A pawn should move two steps forward from its initial position. """
        self.board.place_piece("E2", Piece(PieceType.PAWN, Piece.WHITE))
        self.assertEqual(set(self.board.get_valid_moves("E2")), {"E3", "E4"})

    def test_pawn_cannot_jump(self):
        """ A pawn should not be able to jump over another piece. """
        self.board.place_piece("E2", Piece(PieceType.PAWN, Piece.WHITE))
        self.board.place_piece("E3", Piece(PieceType.PAWN, Piece.BLACK))
        self.assertEqual(set(self.board.get_valid_moves("E2")), set())

    def test_pawn_captures_diagonally(self):
        """ A pawn should capture diagonally if an opponent's piece is there. """
        self.board.place_piece("D4", Piece(PieceType.PAWN, Piece.WHITE))
        self.board.place_piece("C5", Piece(PieceType.PAWN, Piece.BLACK))  # Enemy piece
        self.board.place_piece("E5", Piece(PieceType.PAWN, Piece.BLACK))  # Enemy piece
        self.assertEqual(set(self.board.get_valid_moves("D4")), {"D5", "C5", "E5"})

    def test_pawn_does_not_capture_straight(self):
        """ A pawn should not be able to capture forward. """
        self.board.place_piece("D4", Piece(PieceType.PAWN, Piece.WHITE))
        self.board.place_piece("D5", Piece(PieceType.PAWN, Piece.BLACK))
        self.assertEqual(set(self.board.get_valid_moves("D4")), set())

    def test_pawn_blocked_by_check(self):
        """ A pawn defending the king is blocked by a bishop. """
        self.board.place_piece("D2", Piece(PieceType.PAWN, Piece.WHITE))
        self.board.place_piece("G5", Piece(PieceType.BISHOP, Piece.BLACK))
        self.assertEqual(set(self.board.get_valid_moves("D2")), set())

    def test_pawn_promote(self):
        """A pawn reaching the end of board should have all promote possibilities in his availables move"""
        self.board.place_piece("G7", Piece(PieceType.PAWN, Piece.WHITE))
        self.board.place_piece("H8", Piece(PieceType.BISHOP, Piece.BLACK))
        expected_moves = {"G8K", "G8B", "G8R", "G8Q", "H8K", "H8B", "H8R", "H8Q"}
        self.assertEqual(set(self.board.get_valid_moves("G7")), expected_moves)

    def test_pawn_promote_automatically_transform(self):
        """A pawn reaching the end of board should be automatically transform into knight, bishop, rook or queen"""
        self.board.place_piece("G2", Piece(PieceType.PAWN, Piece.BLACK))
        self.board.move_piece("G2", "G1Q")
        self.assertEqual(self.board.get_piece("G1").kind, PieceType.QUEEN)
        self.assertIsNone(self.board.get_piece("G2"))

    def test_pawn_taken_in_passing(self):
        """when the last move was an adjacent pawn that jumped 2 square,
        you can keep it diagonally with your pawn like he jumped 1 square. """
        self.board.place_piece("G5", Piece(PieceType.PAWN, Piece.WHITE))
        self.board.place_piece("F7", Piece(PieceType.PAWN, Piece.BLACK))
        self.board.move_piece('F7', 'F5')
        expected_move = {"F6", "G6"}
        self.assertEqual(set(self.board.get_valid_moves('G5')), expected_move)
        self.board.move_piece("G5", "F6")
        self.assertIsNone(self.board.get_piece("F5"))
        self.assertIsNone(self.board.get_piece("G5"))
        self.assertEqual(self.board.get_piece("F6").kind, PieceType.PAWN)
        self.assertEqual(self.board.get_piece("F6").color, Piece.WHITE)

    def test_pawn_takin_in_passing(self):
        """taken in passing doesn't work if pawn jump 1 by 1"""
        self.board.place_piece("G5", Piece(PieceType.PAWN, Piece.WHITE))
        self.board.place_piece("F7", Piece(PieceType.PAWN, Piece.BLACK))
        self.board.move_piece('F7', 'F6')
        self.board.move_piece('F6', 'F5')
        expected_move = {"G6"}
        self.assertEqual(set(self.board.get_valid_moves('G5')), expected_move)


if __name__ == "__main__":
    unittest.main()
