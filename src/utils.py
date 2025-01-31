SIZE_BOARD = 8  # Standard chessboard size
FILES = "ABCDEFGH"  # Columns notation in chess

def position_to_coordinates(position: str) -> tuple[int, int]:
    """ Converts a standard chess position (e.g., 'A1') to grid coordinates (row, col). """
    if len(position) not in (2, 3) or position[0] not in FILES or not position[1].isdigit():
        raise ValueError("Invalid chess position format")

    file, rank = position[0], int(position[1])
    col = FILES.index(file)
    row = SIZE_BOARD - rank  # Convert rank to row index (8->0, 7->1, ..., 1->7)
    return row, col

def coordinates_to_position(row: int, col: int) -> str:
    """ Converts grid coordinates (row, col) to a standard chess position (e.g., 'A1'). """
    if not (0 <= row < SIZE_BOARD and 0 <= col < SIZE_BOARD):
        raise ValueError("Coordinates out of bounds")
    return f"{FILES[col]}{SIZE_BOARD - row}"
