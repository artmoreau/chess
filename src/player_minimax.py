import random

from src.board import Board
from src.player import Player


class MinimaxPlayer(Player):
    """ A smarter chess player that evaluates positions and looks ahead a given depth.
        And use of transposition table"""

    WIN_SCORE = 10000
    LOST_SCORE = -WIN_SCORE

    def __init__(self, color: bool, deep_advance: int = 2):
        super().__init__(color)
        self.deep_advance = deep_advance
        # Dictionnaire de table de transposition
        # La clé sera le hash de la position, et la valeur un tuple (depth, score, best_move)
        self._transposition_table: dict[str, tuple[int, int, tuple[str, str] | None]] = {}

    def minimax(self, board: Board, depth: int, alpha: int, beta: int, maximizing: bool) -> tuple[
        int, tuple[str, str] | None]:
        """Version du minimax avec élagage alpha-beta et transposition.

        Args:
            board (Board): La position actuelle.
            depth (int): Profondeur restante d'exploration.
            alpha (int): La borne inférieure de la valeur recherché (pour le maximisateur).
            beta (int): La borne supérieure de la valeur recherchée (pour le minimisateur).
            maximizing (bool): True si c'est le tour du maximisateur, False sinon.

        Returns:
            (int, tuple[str, str] | None): (score évalué, meilleur coup à jouer)
        """
        board_hash = board.get_hash()
        # Vérification dans la table de transposition
        if board_hash in self._transposition_table:
            stored_depth, stored_score, stored_move = self._transposition_table[board_hash]
            if stored_depth >= depth:
                return stored_score, stored_move

        valid_moves = board.get_valid_moves_for_color(board.turn)

        # Cas terminal : profondeur 0 ou absence de coups
        if depth == 0 or not valid_moves:
            if not valid_moves:
                # Cas de mat ou pat
                if board.is_lost(board.turn):
                    score = self.LOST_SCORE if board.turn else self.WIN_SCORE
                else:
                    score = 0
                self._transposition_table[board_hash] = (depth, score, None)
                return score, None

            # Ajustement en cas d'absence de matériel suffisant
            if board.is_ended_by_no_material():
                self._transposition_table[board_hash] = (depth, 0, None)
                return 0, None

            self._transposition_table[board_hash] = (depth, board.score, None)
            return board.score, None

        best_move = None

        if maximizing:
            value = self.LOST_SCORE  # On cherche à maximiser, on démarre avec le plus petit score possible
            for move in valid_moves:
                board.move_piece(*move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.undo_move()
                if eval_score > value:
                    value = eval_score
                    best_move = move
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Coupure beta
            result = (value, best_move)
        else:
            value = self.WIN_SCORE  # Pour minimiser, on démarre avec le plus grand score possible
            for move in valid_moves:
                board.move_piece(*move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.undo_move()
                if eval_score < value:
                    value = eval_score
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Coupure alpha
            result = (value, best_move)

        # Stockage dans la table de transposition pour ne pas recalculer la même position
        self._transposition_table[board_hash] = (depth, result[0], result[1])
        return result

    def choose_move(self, board: Board) -> tuple[str, str] | None:
        """ Selects the best move based on the minimax evaluation. """
        score, best_move = self.minimax(board, self.deep_advance, self.LOST_SCORE, self.WIN_SCORE, True)
        if best_move:
            return best_move
        else:
            valid_moves = board.get_valid_moves_for_color(board.turn)
            return random.choice(valid_moves) if valid_moves else None
