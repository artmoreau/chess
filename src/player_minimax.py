import random

from src.board import Board
from src.player import Player


class MinimaxPlayer(Player):
    """ A smarter chess player that evaluates positions and looks ahead a given depth. """

    WIN_SCORE = 10000
    LOST_SCORE = -WIN_SCORE

    def __init__(self, color: bool, deep_advance: int = 2):
        super().__init__(color)
        self.deep_advance = deep_advance

    def minimax(self, board: Board, depth: int, maximizing: bool) -> tuple[int, tuple[str, str] | None]:
        """ Minimax algorithm with depth limit to evaluate the best move. """
        valid_moves = board.get_valid_moves_for_color(board.turn)

        if depth == 0 or not valid_moves:
            if not valid_moves:  # checkmate or pat
                if board.is_lost(board.turn):
                    return (self.LOST_SCORE, None) if board.turn else (self.WIN_SCORE, None)
                return 0, None

            if board.is_ended_by_no_material():
                return 0, None

            return board.score, None

        best_move = None
        if maximizing:
            max_eval = self.LOST_SCORE
            for move in valid_moves:
                board.move_piece(*move)
                eval_score, _ = self.minimax(board, depth - 1, False)
                board.undo_move()
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = self.WIN_SCORE
            for move in valid_moves:
                board.move_piece(*move)
                eval_score, _ = self.minimax(board, depth - 1, True)
                board.undo_move()
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval, best_move

    def choose_move(self, board: Board) -> tuple[str, str] | None:
        """ Selects the best move based on the minimax evaluation. """
        _, best_move = self.minimax(board, self.deep_advance, True)
        return best_move if best_move else random.choice(board.get_valid_moves_for_color(board.turn))
