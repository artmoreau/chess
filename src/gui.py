import os
import pygame


# screen and box format
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE, BLACK = (255, 255, 255), (120, 80, 50)

# Init pygame
def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    return screen


base_path = os.path.dirname(os.path.abspath(__file__))  # current script path
assets_path = os.path.join(base_path, "../assets/pieces")  # path to images folder


# Load images
piece_images = {
    "P": pygame.image.load(os.path.join(assets_path, "white_pawn.png")),
    "p": pygame.image.load(os.path.join(assets_path, "black_pawn.png")),
    "N": pygame.image.load(os.path.join(assets_path, "white_knight.png")),
    "n": pygame.image.load(os.path.join(assets_path, "black_knight.png")),
    "B": pygame.image.load(os.path.join(assets_path, "white_bishop.png")),
    "b": pygame.image.load(os.path.join(assets_path, "black_bishop.png")),
    "R": pygame.image.load(os.path.join(assets_path, "white_rook.png")),
    "r": pygame.image.load(os.path.join(assets_path, "black_rook.png")),
    "Q": pygame.image.load(os.path.join(assets_path, "white_queen.png")),
    "q": pygame.image.load(os.path.join(assets_path, "black_queen.png")),
    "K": pygame.image.load(os.path.join(assets_path, "white_king.png")),
    "k": pygame.image.load(os.path.join(assets_path, "black_king.png")),
}

# resize the images
for key in piece_images:
    piece_images[key] = pygame.transform.scale(piece_images[key], (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen):
    """Draw chess board"""
    colors = [WHITE, BLACK]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
    """Draw piece on board"""
    for row in range(8):
        for col in range(8):
            piece = board.grid[row][col]
            if piece:
                symbol = piece.symbol()
                piece_img = piece_images.get(symbol, None)
                if piece_img:
                    screen.blit(piece_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def update_display(screen, board):
    """Updtade screen display"""
    draw_board(screen)
    draw_pieces(screen, board)
    pygame.display.flip()
