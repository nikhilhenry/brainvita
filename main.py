import pygame
import constants as c
from board import Board

# initialize pygame
pygame.init()


class Marble(pygame.sprite.Sprite):
    pass


class Brainvita:
    """
    Game instance. To reset the game, create a new instance.
    """

    def __init__(self):

        # Game state
        self.board = Board()
        self.is_game_over = False

        # Create sprite lists
        self.marble_list = pygame.sprite.Group()

        # Create the marble sprites
        for i in range(self.board.num_marbles):
            marble = Marble()
            # marble.assign_position(self.board.get_position(i))
            self.marble_list.add(marble)

    def process_events(self) -> None:
        """
        Process all events
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

    def main_loop(self):
        """
        Main game loop for Brainvita. Run this in the main loop.
        """

        # draw other things
        # Move all the sprites
        self.marble_list.update()

    def display(self):
        """
        Display the game state
        """

        c.ROOT_DISPLAY.fill(c.CLR_BACKGROUND)

        # draw the board
        c.ROOT_DISPLAY.blit(
            c.SPRT_BOARD,
            (
                c.D_WIDTH // 2 - (c.SPRT_BOARD.get_width() // 2),
                c.D_HEIGHT // 2 - (c.SPRT_BOARD.get_height() // 2),
            ),
        )

        rendered_text = c.FONT_MAIN.render("Brainvita", False, (0, 0, 0))
        c.ROOT_DISPLAY.blit(
            rendered_text,
            (
                20,
                50,
            ),
        )
        rendered_text = c.FONT_UI.render("Moves:        0", False, (0, 0, 0))
        c.ROOT_DISPLAY.blit(
            rendered_text,
            (
                20,
                120,
            ),
        )
        rendered_text = c.FONT_UI.render(f"Marbles:    {self.board.num_marbles}", False, (0, 0, 0))
        c.ROOT_DISPLAY.blit(
            rendered_text,
            (
                20,
                150,
            ),
        )
        # self.marble_list.draw(c.ROOT_DISPLAY)

        pygame.display.flip()


def main():
    """Main program function."""

    game = Brainvita()

    # Main game loop
    while not game.is_game_over:

        # Process events (keystrokes, mouse clicks, etc)
        game.process_events()
        # Update object positions, run game logic
        game.main_loop()
        # Draw the current frame
        game.display()
        c.GAME_CLOCK.tick(c.TICK_RATE)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
