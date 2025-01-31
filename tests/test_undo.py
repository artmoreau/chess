import unittest
from copy import deepcopy

from src.board import Board
from src.piece import Piece, PieceType


class TestUndo(unittest.TestCase):

    def setUp(self):
        """ Sets up an empty board before each test """
        self.board = Board()

    def test_undo_basic_moves(self):
        self.board.initialize_standard_board()
        initial_board = deepcopy(self.board)
        self.board.move_piece("E2", "E4")
        self.board.undo_move()
        self.assertEqual(initial_board, self.board)

    def test_undo_capture(self):
        self.board.place_piece("D4", Piece(PieceType.BISHOP, Piece.WHITE))
        self.board.place_piece("F6", Piece(PieceType.PAWN, Piece.BLACK))
        initial_board = deepcopy(self.board)
        self.board.move_piece("D4", "F6")
        self.board.undo_move()
        self.assertEqual(initial_board, self.board)

    def test_undo_promote(self):
        pawn = Piece(PieceType.PAWN, Piece.BLACK)
        pawn.mark_as_moved()
        self.board.place_piece("G2", pawn)
        initial_board = deepcopy(self.board)
        self.board.move_piece("G2", "G1Q")
        self.board.undo_move()
        self.assertEqual(initial_board, self.board)

    def test_undo_castle(self):
        self.board.place_piece("E8", Piece(PieceType.KING, Piece.BLACK))
        self.board.place_piece("E1", Piece(PieceType.KING, Piece.WHITE))
        self.board.place_piece("A1", Piece(PieceType.ROOK, Piece.WHITE))
        initial_board = deepcopy(self.board)
        self.board.move_piece("E1", "C1")
        self.board.undo_move()
        self.assertEqual(initial_board, self.board)

    def test_undo_en_passant(self):
        self.board.place_piece("G5", Piece(PieceType.PAWN, Piece.WHITE))
        self.board.place_piece("F7", Piece(PieceType.PAWN, Piece.BLACK))
        self.board.move_piece('F7', 'F5')
        initial_board = deepcopy(self.board)
        self.board.move_piece("G5", "F6")
        self.board.undo_move()
        self.assertEqual(initial_board, self.board)


if __name__ == "__main__":
    unittest.main()