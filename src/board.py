from __future__ import annotations
from copy import deepcopy
from typing import Optional

from src.piece import Piece, PieceType
from src.utils import (
    SIZE_BOARD,
    FILES,
    position_to_coordinates,
    coordinates_to_position
)


class Board:

    def __init__(self):
        """ Initializes an empty chessboard (8x8) with None in each cell. """
        self.grid : list[list[Optional[Piece]]] = [[None for _ in range(SIZE_BOARD)] for _ in range(SIZE_BOARD)]
        self._white_king_pos = None
        self._black_king_pos = None
        self._last_move = (None, None)
        self._turn = Piece.WHITE
        self._score = 0
        self.history = []

    @property
    def white_king_pos(self) -> str:
        return self._white_king_pos

    @property
    def black_king_pos(self) -> str:
        return self._black_king_pos

    @property
    def last_move(self) -> tuple[Optional[str], Optional[str]]:
        return self._last_move

    @property
    def turn(self) -> bool:
        return self._turn

    @property
    def score(self) -> int:
        return self._score

    def set_white_king_pos(self, position: str) -> None:
        self._white_king_pos = position

    def set_black_king_pos(self, position: str) -> None:
        self._black_king_pos = position

    def set_last_move(self, initial_position: str, final_position: str) -> None:
        self._last_move = (initial_position, final_position)

    def set_score(self, score: int) -> None:
        self._score = score

    def swap_turn(self):
        self._turn = not self._turn

    def place_piece(self, position: str, piece: Piece):
        """ Places a piece at a given position in chess notation (e.g., 'E2'). """
        row, col = position_to_coordinates(position)
        self.grid[row][col] = piece

        if piece.kind == PieceType.KING:
            if piece.color == Piece.WHITE:
                self.set_white_king_pos(position)
            else:
                self.set_black_king_pos(position)

    def remove_piece(self, position: str) -> None:
        """ Removes a piece from the board at the given position. """
        row, col = position_to_coordinates(position)
        self.grid[row][col] = None

    def move_piece(self, initial_position: str, final_position) -> None:
        """ play the move defined by initial_position and final_position. """

        piece = self.get_piece(initial_position)
        if not piece:  # Should never append in a classic game
            raise ValueError(f"There is no piece at the position {initial_position}")

        captured_piece = self.get_piece(final_position)
        is_taking_en_passant = (
            piece.kind == PieceType.PAWN and
            initial_position[0] != final_position[0] and
            captured_piece is None
        )
        captured_position = final_position if not is_taking_en_passant else final_position[0] + initial_position[1]
        captured_piece = self.get_piece(captured_position)

        is_promotion = len(final_position) == 3
        is_roque = piece.kind == PieceType.KING and initial_position[0] == 'E' and final_position[0] in ('C', 'G')

        self.history.append(
            (initial_position, final_position, deepcopy(piece), captured_piece, is_taking_en_passant, is_promotion, is_roque,
             self.white_king_pos, self.black_king_pos, self.last_move, self.score)
        )

        if captured_piece:
            self.set_score(self.score - captured_piece.score)

        self.place_piece(final_position, piece)
        self.remove_piece(initial_position)
        piece.mark_as_moved()
        self.set_last_move(initial_position, final_position)

        # it's a rock, move the rook too
        if is_roque:
            # Compute rook start_position
            rook_start_first_position = 'A' if final_position[0] == 'C' else 'H'
            rook_start_second_position =  initial_position[1]
            rook_start_position = rook_start_first_position + rook_start_second_position
            # Compute rook end_position
            rook_end_first_position = 'D' if final_position[0] == 'C' else 'F'
            rook_end_second_position =  initial_position[1]
            rook_end_position = rook_end_first_position + rook_end_second_position
            # Move the rook
            rook = self.get_piece(rook_start_position)
            self.place_piece(rook_end_position, rook)
            self.remove_piece(rook_start_position)
            rook.mark_as_moved()

        elif piece.kind == PieceType.PAWN:  # it's a pawn
            if is_promotion:  # it's a promotion
                kind_dict = {
                    'K': PieceType.KNIGHT,
                    'B': PieceType.BISHOP,
                    'R': PieceType.ROOK,
                    'Q': PieceType.QUEEN,
                }
                new_piece = Piece(kind_dict.get(final_position[2]), piece.color)
                removed_pawn_score = Piece.piece_values[PieceType.PAWN] * 1 if piece.color == Piece.WHITE else -1
                self.place_piece(final_position, new_piece)
                self.set_score(self.score + new_piece.score - removed_pawn_score)

            elif is_taking_en_passant: # it's a taken en passant
                # remove the piece taken
                self.remove_piece(captured_position)

        self.swap_turn()

    def undo_move(self):
        """ Undoes the last move played, restoring special cases like promotion, roque and en passant. """
        if not self.history:
            return

        (initial_position, final_position, piece, captured_piece, is_taking_en_passant, is_promotion, is_roque,
         white_king_pos, black_king_pos, last_move, score) = self.history.pop()

        self.set_white_king_pos(white_king_pos)
        self.set_black_king_pos(black_king_pos)
        self.set_last_move(*last_move)
        self.set_score(score)

        if is_roque:
            if final_position == "G1":  # Roque white kingside
                rook = self.get_piece("F1")
                self.place_piece("E1", piece)
                self.place_piece("H1", rook)
                piece.unmark_as_moved()
                rook.unmark_as_moved()
                self.remove_piece("G1")
                self.remove_piece("F1")

            elif final_position == "C1":  # Roque white queenside
                rook = self.get_piece("D1")
                self.place_piece("E1", piece)
                self.place_piece("A1", rook)
                piece.unmark_as_moved()
                rook.unmark_as_moved()
                self.remove_piece("C1")
                self.remove_piece("D1")

            elif final_position == "G8":  # Roque black kingside
                rook = self.get_piece("F8")
                self.place_piece("E8", piece)
                self.place_piece("H8", rook)
                piece.unmark_as_moved()
                rook.unmark_as_moved()
                self.remove_piece("G8")
                self.remove_piece("F8")

            elif final_position == "C8":  # Roque black queenside
                rook = self.get_piece("D8")
                self.place_piece("E8", piece)
                self.place_piece("A8", rook)
                piece.unmark_as_moved()
                rook.unmark_as_moved()
                self.remove_piece("C8")
                self.remove_piece("D8")

            self.swap_turn()
            return  # nothing else to do

        if is_promotion:
            # Set last pawn on his place
            original_pawn = Piece(PieceType.PAWN, piece.color)
            original_pawn.mark_as_moved()
            self.place_piece(initial_position, original_pawn)
        else:
            self.place_piece(initial_position, piece)

        if captured_piece:
            if is_taking_en_passant:
                captured_position = final_position[0] + initial_position[1]
                self.place_piece(captured_position, captured_piece)
                self.remove_piece(final_position)
            else:
                self.place_piece(final_position, captured_piece)
        else:
            self.remove_piece(final_position)

        self.swap_turn()

    def get_piece(self, position: str) -> Optional[Piece]:
        """ Returns the piece at a given position, or None if the square is empty. """
        row, col = position_to_coordinates(position)
        return self.grid[row][col]

    def get_pieces(self, color: Optional[bool] = None) -> list[tuple[Piece, str]]:
        """ Returns all pieces on the board with their positions.
            If 'color' is specified, only returns the color pieces.
        """
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and (color is None or piece.color == color):
                    position = coordinates_to_position(row, col)
                    pieces.append((piece, position))
        return pieces

    def is_empty(self, position: str) -> bool:
        """ Checks if a given position is empty. """
        return self.get_piece(position) is None

    def is_under_attack(self, position: str, color: bool) -> bool:
        """ Checks if the given position is attack by piece of color. """
        for _, enemy_pos in self.get_pieces(color=color):
            if position in self.get_threat(enemy_pos):
                return True  # The position is under attack
        return False

    def is_path_under_attack(self, positions: list[str], color: bool) -> bool:
        """Checks if any position in the given list is under attack by piece of color. """
        return any(self.is_under_attack(pos, color) for pos in positions)

    def find_king(self, color: bool) -> str:
        """ Finds the position of the king of the given color. Raise ValueError if not found. """
        return self.white_king_pos if color == Piece.WHITE else self.black_king_pos

    def is_king_in_ckeck(self, color) -> bool:
        """Check if the king of the given color is in check"""
        king_postion = self.find_king(color)
        return self.is_under_attack(king_postion, not color)

    def initialize_standard_board(self):
        """ Sets up the chessboard in its standard starting position. """
        # Place major pieces
        for col, piece in enumerate([PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP,
                                     PieceType.QUEEN, PieceType.KING, PieceType.BISHOP,
                                     PieceType.KNIGHT, PieceType.ROOK]):
            self.place_piece(f"{FILES[col]}1", Piece(piece, Piece.WHITE))
            self.place_piece(f"{FILES[col]}8", Piece(piece, Piece.BLACK))

        # Place pawns
        for col in range(SIZE_BOARD):
            self.place_piece(f"{FILES[col]}2", Piece(PieceType.PAWN, Piece.WHITE))
            self.place_piece(f"{FILES[col]}7", Piece(PieceType.PAWN, Piece.BLACK))

        self.set_white_king_pos('E1')
        self.set_black_king_pos('E8')

    def __str__(self) -> str:
        """ Returns a textual representation of the chessboard. """
        board_str = "\n  A B C D E F G H\n"  # Column headers
        for row in range(SIZE_BOARD):
            board_str += f"{SIZE_BOARD - row} "  # Row numbers
            for col in range(SIZE_BOARD):
                piece = self.grid[row][col]
                board_str += (piece.symbol_log() if piece else "◦") + " "
            board_str += f"{SIZE_BOARD - row}\n"  # Row numbers on the right side
        board_str += "  A B C D E F G H"  # Column headers
        return board_str

    def get_valid_moves_for_color(self, color: bool) -> list[tuple[str, str]]:
        """return the list of all valid move for the color"""
        valid_moves = []
        for _, pos in self.get_pieces(color):
            valid_end_points_for_pos = self.get_valid_moves(pos)
            for valid_end_point_for_pos in valid_end_points_for_pos:
                valid_moves.append((pos, valid_end_point_for_pos))
        return valid_moves

    def is_lost(self, color):
        """return True if it's lost by checkmate False for draw. can make sens only
        if self.get_valid_moves_for_color(color) == [] """
        return self.is_king_in_ckeck(color)

    def is_ended_by_no_material(self):
        """return True if they are no more materials to win the game"""
        for piece, _ in self.get_pieces():
            if piece.kind in (PieceType.PAWN, PieceType.ROOK, PieceType.QUEEN):
                return False

        for color in (Piece.WHITE, Piece.BLACK):
            count_secondary_piece = 0
            for piece, _ in self.get_pieces(color):
                if piece.kind in (PieceType.KING, PieceType.BISHOP):
                    count_secondary_piece += 1
                    if count_secondary_piece >= 2:
                        return False
        return True


    # ---- Implementation of each piece's threat and moves ----

    def get_threat(self, position: str) -> list[str]:
        """ Returns the threat squares controlled by the piece at the given position. """
        kind = self.get_piece(position).kind

        threats_dict = {
            PieceType.PAWN: lambda pos: self._pawn_threat(pos),
            PieceType.KNIGHT: lambda pos: self._knight_threat(pos),
            PieceType.BISHOP: lambda pos: self._bishop_threat(pos),
            PieceType.ROOK: lambda pos: self._rook_threat(pos),
            PieceType.QUEEN: lambda pos: self._queen_threat(pos),
            PieceType.KING: lambda pos: self._king_threat(pos),
        }

        return threats_dict[kind](position)

    def get_valid_moves(self, position: str) -> list[str]:
        """ Returns a list of valid moves for the piece at the given position for the board (self). """
        piece = self.get_piece(position)
        if not piece:
            raise ValueError(f"There is no piece at the position f{position}")

        kind = piece.kind
        color = piece.color

        threats_dict = {
            PieceType.PAWN: lambda pos: self._pawn_moves(pos),
            PieceType.KNIGHT: lambda pos: self._knight_moves(pos),
            PieceType.BISHOP: lambda pos: self._bishop_moves(pos),
            PieceType.ROOK: lambda pos: self._rook_moves(pos),
            PieceType.QUEEN: lambda pos: self._queen_moves(pos),
            PieceType.KING: lambda pos: self._king_moves(pos),
        }

        moves = threats_dict[kind](position)
        # filter moves that make our king into check
        valid_moves = []
        for final_pos in moves:
            self.move_piece(initial_position=position, final_position=final_pos)
            if not self.is_king_in_ckeck(color):
                valid_moves.append(final_pos)
            self.undo_move()
        return valid_moves

    def get_moves_from_threat(self, position: str, threat : list[str]) -> list[str]:
        """helper function to convert threat to move. """
        color = self.get_piece(position).color
        return [move for move in threat if not self.get_piece(move) or self.get_piece(move).color != color]

    def _pawn_threat(self, position: str) -> list[str]:
        """ Returns the threat squares controlled by the pawn. """
        threats = []
        row, col = position_to_coordinates(position)
        color = self.get_piece(position).color
        direction = -1 if color else 1  # White moves up, Black moves down

        for dc in [-1, 1]:
            diag_col = col + dc
            if 0 <= diag_col < 8:
                diag_row = row + direction
                # Only add the diagonal positions that are within bounds
                if 0 <= diag_row < 8:
                    diag_pos = coordinates_to_position(diag_row, diag_col)
                    threats.append(diag_pos)
        return threats

    def _pawn_moves(self, position: str) -> list[str]:
        color = self.get_piece(position).color
        direction = -1 if color == Piece.WHITE else 1  # White moves up, Black moves down

        # filter move to keep from self.pawn_threat(position)
        moves = []
        for move in self._pawn_threat(position):
            if self.get_piece(move) and self.get_piece(move).color != color:
                moves.append(move)

            elif color == Piece.WHITE and position[1] == '5':
                col = move[0]
                valid_last_move = (f'{col}7', f'{col}5')
                if self.last_move == valid_last_move:
                    moves.append(move)

            elif color == Piece.BLACK and position[1] == '4':
                col = move[0]
                valid_last_move = (f'{col}2', f'{col}4')
                if self.last_move == valid_last_move:
                    moves.append(move)


        # Move forward
        row, col = position_to_coordinates(position)
        forward_pos = coordinates_to_position(row + direction, col)
        if self.is_empty(forward_pos):
            moves.append(forward_pos)

            # Double move on first move
            if (color == Piece.WHITE and row == 6) or (color == Piece.BLACK and row == 1):
                double_forward = coordinates_to_position(row + 2 * direction, col)
                if self.is_empty(double_forward):
                    moves.append(double_forward)

        # check if pawn is on the last row of the board and add all promote possibilities
        promotes_moves = []
        for move in moves:
            if (color == Piece.WHITE and move[1] == '8') or (color == Piece.BLACK and move[1] == '1'):
                for promote_letter in ('K', 'B', 'R', 'Q'):
                    promotes_moves.append(move + promote_letter)
            else:
                promotes_moves.append(move)

        return promotes_moves

    @staticmethod
    def _knight_threat(position: str) -> list[str]:
        """ Returns the threat squares controlled by the knight. """
        threats = []
        row, col = position_to_coordinates(position)

        # All possible "L" shaped moves for the knight
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                new_pos = coordinates_to_position(new_row, new_col)
                threats.append(new_pos)

        return threats

    def _knight_moves(self, position: str) -> list[str]:
        """ Returns the possible moves for a bishop. """
        return self.get_moves_from_threat(position, self._knight_threat(position))

    def _traverse_directions(self, position: str, directions: list[tuple[int, int]]) -> list[str]:
        """ Generic function for traversing multiple directions (used by bishops, rooks, queens). """
        threat = []
        row, col = position_to_coordinates(position)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                new_pos = coordinates_to_position(new_row, new_col)
                piece = self.get_piece(new_pos)
                threat.append(new_pos)
                if piece:
                    break  # Stop if piece blocks path
                new_row += dr
                new_col += dc

        return threat

    def _bishop_threat(self, position: str) -> list[str]:
        """ Returns the threat squares controlled by the bishop. """
        return self._traverse_directions(position, [(1, 1), (1, -1), (-1, 1), (-1, -1)])

    def _bishop_moves(self, position: str) -> list[str]:
        """ Returns the possible moves for a bishop. """
        return self.get_moves_from_threat(position, self._bishop_threat(position))

    def _rook_threat(self, position: str) -> list[str]:
        """ Returns the threat squares controlled by the rook. """
        return self._traverse_directions(position, [(1, 0), (-1, 0), (0, 1), (0, -1)])

    def _rook_moves(self, position: str) -> list[str]:
        """ Returns the possible moves for a rook. """
        return self.get_moves_from_threat(position, self._rook_threat(position))

    def _queen_threat(self, position: str) -> list[str]:
        """ Returns the threat squares controlled by the queen. """
        return self._bishop_threat(position) + self._rook_threat(position)

    def _queen_moves(self, position: str) -> list[str]:
        """ Returns the possible moves for a queen. """
        return self.get_moves_from_threat(position, self._queen_threat(position))

    @staticmethod
    def _king_threat(position: str) -> list[str]:
        """ Returns the threat squares controlled by the king. """
        threats = []
        row, col = position_to_coordinates(position)

        # All possible moves for the king (1 square in any direction)
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                new_pos = coordinates_to_position(new_row, new_col)
                threats.append(new_pos)

        return threats


    def _king_moves(self, position: str) -> list[str]:
        """ Returns the possible moves for a king. """
        moves = self.get_moves_from_threat(position, self._king_threat(position))

        piece = self.get_piece(position)
        color = piece.color

        if not piece.has_moved and not self.is_king_in_ckeck(color):
            row, col = position_to_coordinates(position)
            rook_positions = [("A", 0), ("H", 7)]  # Queenside and Kingside

            for file, rook_col in rook_positions:
                rook_pos = f"{file}{SIZE_BOARD - row}"
                rook = self.get_piece(rook_pos)

                if rook and rook.kind == PieceType.ROOK and not rook.has_moved:
                    # Check if path between king and rook is clear
                    step = 1 if rook_col > col else -1
                    path = [coordinates_to_position(row, c) for c in range(col + step, rook_col, step)]

                    if all(self.is_empty(pos) for pos in path) and not self.is_path_under_attack(path, not color):
                        moves.append(coordinates_to_position(row, col + 2 * step))  # Castling move
        return moves

    def __eq__(self, other: Board):

        if self.white_king_pos != other.white_king_pos:
            return False
        if self.black_king_pos != other.black_king_pos:
            return False
        if self.turn != other.turn:
            return False
        if self.last_move != other._last_move:
            return False
        if self.score != other.score:
            print("score differ")
            return False

        for (spiece, spos), (opiece, opos) in zip(self.get_pieces(), other.get_pieces()):
            if spos != opos:
                return False
            if spiece.kind != opiece.kind:
                return False
            if spiece.color != opiece.color:
                return False
            if spiece.has_moved != opiece.has_moved:
                return False

        return True

    def get_hash(self) -> str:
        """
        Calcule une représentation unique de la position.
        On utilise ici la grille (en indiquant le type, la couleur et si une pièce a bougé)
        ainsi que le tour et le dernier coup.
        """

        rows = []
        for row in range(len(self.grid)):
            row_repr = []
            for col in range(len(self.grid[row])):
                piece = self.grid[row][col]
                if piece:
                    # Un identifiant pour la pièce, par exemple "KWM" pour un roi blanc ayant bougé ("M" pour moved, "0" sinon)
                    moved = "M" if piece.has_moved else "0"
                    color = "W" if piece.color == Piece.WHITE else "B"
                    row_repr.append(piece.kind.value[0] + color + moved)
                else:
                    row_repr.append("___")
            rows.append("|".join(row_repr))
        # Incluant le tour et le dernier coup dans la clé
        return "|".join(rows) + f":{self._turn}" + f":{self._last_move}"
