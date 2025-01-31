import logging
import pygame

from src.board import Board
from src.player import Player
from src.gui import update_display, init_pygame


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class Controller:
    """ Controls the game flow between two BasicPlayers. """

    def __init__(self, player1: Player, player2: Player):
        self.board = Board()
        self.board.initialize_standard_board()
        self.players = {
            True: player1,  # White
            False: player2 # Black
        }
        self.current_turn = True  # White starts

        # Init pygame
        self.screen = init_pygame()

    def play_game(self):
        """ Runs a full game simulation until a termination condition is met. """
        logger.info(f"Game Started :")
        logger.info(self.board)
        move_count = 0

        while True:

            # Manage pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            # Draw chess board
            update_display(self.screen, self.board)

            player = self.players[self.current_turn]
            move = player.choose_move(self.board)

            if move is None:
                if self.board.is_lost(self.current_turn):
                    logger.info(f"Checkmate! {'White' if not self.current_turn else 'Black'} wins!")
                else:
                    logger.info("Stalemate! It's a draw.")
                break

            # Execute the move
            self.board.move_piece(*move)

            move_count += 1
            self.current_turn = not self.current_turn  # Switch turns

            logger.info(self.board)

            # Check for no-material end condition
            if self.board.is_ended_by_no_material():
                logger.info("Draw by insufficient material!")
                break

        logger.info(f"Game over in {move_count} moves.")
