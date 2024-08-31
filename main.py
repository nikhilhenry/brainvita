import asyncio
from typing import Any, TextIO
import pygame
import constants as c
from board import Board, Move, NodeState
from collections import namedtuple
from music_controller import MusicController
import sys
import platform
from utils import Position
import argparse

import widgets

Coordinate = namedtuple("Coordinate", ["x", "y"])

# Mapping of board position to coordinates
POS2COORD = {}
for i in range(7):
    for j in range(7):
        # 198x198 board, 18x18 marbles, 36x36 is the padding before grid starts, no padding in between marbles
        POS2COORD[Position(i, j)] = Coordinate(
            ((c.D_WIDTH // 2) - (198 * c.SCALE_FACTOR // 2))
            + (36 * c.SCALE_FACTOR)
            + (j * 18 * c.SCALE_FACTOR),
            ((c.D_HEIGHT // 2) - (198 * c.SCALE_FACTOR // 2))
            + (36 * c.SCALE_FACTOR)
            + (i * 18 * c.SCALE_FACTOR),
        )

# initialize pygame
pygame.init()


class Marble(pygame.sprite.Sprite):
    def __init__(self, pos: Position, state: NodeState):
        super().__init__()

        self.image = c.SPRT_MARBLE
        self.rect = self.image.get_rect()

        self.pos = pos
        self.state = state

        # initial rect location
        if self.state == NodeState.FILLED:
            self.rect.x = POS2COORD[self.pos].x
            self.rect.y = POS2COORD[self.pos].y
        else:
            self.rect.x = -100
            self.rect.y = -100

    def update(self, new_pos: Position, state: NodeState) -> None:
        self.state = state
        if self.state == NodeState.FILLED:
            self.pos = new_pos
            self.rect.x = POS2COORD[self.pos].x
            self.rect.y = POS2COORD[self.pos].y
        else:
            self.rect.x = -100
            self.rect.y = -100


class Brainvita:
    """
    Game instance. To reset the game, create a new instance.
    """

    def __init__(
        self, musician: MusicController, starting_state: str | None = None
    ) -> None:

        # Game state
        if starting_state is not None:
            self.board = Board.construct_from_string(starting_state)
        else:
            self.board = Board()

        self.move_count = 0
        self.is_game_over = False
        self.selected_marble = None
        self.possible_positions = []

        # musician
        self.musician = musician
        self.musician.start()

        # Create sprite lists
        self.marble_list = pygame.sprite.Group()

        # Create the marble sprites
        for pos in self.board._board:
            marble = Marble(pos, state=self.board._board[pos])
            self.marble_list.add(marble)

        # Create the buttons
        self.reset_button = widgets.ImageButton(
            (20, 200),
            c.SPRT_BTN,
            hovered_surface=c.SPRT_BTN_HOVERED,
            clicked_surface=c.SPRT_BTN_CLICKED,
        )
        self.dfs_button = widgets.ImageButton(
            (20, 250),
            c.SPRT_BTN,
            hovered_surface=c.SPRT_BTN_HOVERED,
            clicked_surface=c.SPRT_BTN_CLICKED,
        )
        self.bfs_button = widgets.ImageButton(
            (20, 300),
            c.SPRT_BTN,
            hovered_surface=c.SPRT_BTN_HOVERED,
            clicked_surface=c.SPRT_BTN_CLICKED,
        )
        self.bestfs_button = widgets.ImageButton(
            (20, 350),
            c.SPRT_BTN,
            hovered_surface=c.SPRT_BTN_HOVERED,
            clicked_surface=c.SPRT_BTN_CLICKED,
        )
        self.mute_button = widgets.ImageButton(
            (20, 400),
            c.SPRT_BTN,
            hovered_surface=c.SPRT_BTN_HOVERED,
            clicked_surface=c.SPRT_BTN_CLICKED,
        )
        self.unmute_button = widgets.ImageButton(
            (200, 400),
            c.SPRT_BTN,
            hovered_surface=c.SPRT_BTN_HOVERED,
            clicked_surface=c.SPRT_BTN_CLICKED,
        )
        self.undo_button = widgets.ImageButton(
            (20, 450),
            c.SPRT_BTN,
            hovered_surface=c.SPRT_BTN_HOVERED,
            clicked_surface=c.SPRT_BTN_CLICKED,
        )
        self.button_list = pygame.sprite.Group()
        self.button_list.add(
            self.reset_button,
            self.dfs_button,
            self.bfs_button,
            self.bestfs_button,
            self.mute_button,
            self.unmute_button,
            self.undo_button,
        )

    def process_events(self) -> None:
        """
        Process all events
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_over = True
            if event.type == pygame.MOUSEMOTION:
                # update button hover state
                for button in self.button_list:
                    button.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get which marble is hovered and clicked (if any)
                for marble in self.marble_list:
                    if marble.rect.collidepoint(event.pos):
                        # mark marble as selected, prompting move generation
                        self.selected_marble = marble
                        self.musician.play_select_sound()
                
                # get which possible move is clicked (if any)
                for move in self.possible_positions:
                    if (
                        POS2COORD[move].x
                        < event.pos[0]
                        < POS2COORD[move].x + 18 * c.SCALE_FACTOR
                    ):
                        if (
                            POS2COORD[move].y
                            < event.pos[1]
                            < POS2COORD[move].y + 18 * c.SCALE_FACTOR
                        ):
                            # move the marble
                            new_board = self.board.make_move(
                                Move(self.selected_marble.pos, move)
                            )
                            if new_board:
                                self.musician.play_move_sound()
                                self.board = new_board
                                self.move_count += 1
                                self.update_marbles_based_on_board()
                                self.selected_marble = None
                                self.possible_positions = []
                
                # get which button is clicked (if any)
                button: widgets.ImageButton
                for button in self.button_list:
                    if button.hovered:
                        button.is_clicked = True

    def update_marbles_based_on_board(self):
        """
        Update the marbles based on the board state
        """
        for marble in self.marble_list:
            marble.update(marble.pos, self.board[marble.pos])

    def main_loop(self):
        """
        Main game loop for Brainvita.
        """

        if self.selected_marble:
            move_locations = self.board.get_possible_move_locations(
                self.selected_marble.pos
            )
            self.possible_positions = move_locations
        
    
        if self.reset_button.is_clicked:
            self.board = Board()
            self.move_count = 0
            self.update_marbles_based_on_board()
            self.selected_marble = None
            self.possible_positions = []
            self.reset_button.is_clicked = False
        elif self.dfs_button.is_clicked:
            # self.board = self.board.solve_dfs()
            # self.update_marbles_based_on_board()
            self.dfs_button.is_clicked = False
        elif self.bfs_button.is_clicked:
            # self.board = self.board.solve_bfs()
            # self.update_marbles_based_on_board()
            self.bfs_button.is_clicked = False
        elif self.bestfs_button.is_clicked:
            # self.board = self.board.solve_bestfs()
            # self.update_marbles_based_on_board()
            self.bestfs_button.is_clicked = False
        elif self.mute_button.is_clicked:
            self.musician.mute()
            self.mute_button.is_clicked = False
        elif self.unmute_button.is_clicked:
            self.musician.unmute()
            self.unmute_button.is_clicked = False
        elif self.undo_button.is_clicked:
            # if self.move_count > 0:
            #     self.board = self.board.undo()
            #     self.move_count -= 1
            #     self.update_marbles_based_on_board()
            self.undo_button.is_clicked = False

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
        c.ROOT_DISPLAY.blit(rendered_text, (20, 50))
        rendered_text = c.FONT_UI.render(
            f"Moves:        {self.move_count}", False, (0, 0, 0)
        )
        c.ROOT_DISPLAY.blit(rendered_text, (20, 120))
        rendered_text = c.FONT_UI.render(
            f"Marbles:    {self.board.num_marbles}", False, (0, 0, 0)
        )
        c.ROOT_DISPLAY.blit(rendered_text, (20, 150))

        self.marble_list.draw(c.ROOT_DISPLAY)

        if self.selected_marble:
            c.ROOT_DISPLAY.blit(
                c.SPRT_SELECTED_MARBLE,
                (self.selected_marble.rect.x, self.selected_marble.rect.y),
            )
        if self.possible_positions:
            for move in self.possible_positions:
                c.ROOT_DISPLAY.blit(
                    c.SPRT_POSSIBLE_MOVE,
                    (POS2COORD[move].x, POS2COORD[move].y),
                )

        self.button_list.draw(c.ROOT_DISPLAY)
        pygame.display.flip()


async def main(starting_state: str | None = None):
    """Main program function."""

    musician = MusicController()
    game = Brainvita(musician=musician, starting_state=starting_state)

    if sys.platform == "emscripten":  # for web
        platform.window.canvas.style.imageRendering = "pixelated"

    # Main game loop
    while not game.is_game_over:

        # Process events (keystrokes, mouse clicks, etc)
        game.process_events()
        # Update object positions, run game logic
        game.main_loop()
        # Draw the current frame
        game.display()
        c.GAME_CLOCK.tick(c.TICK_RATE)
        await asyncio.sleep(0)

    # Close window and exit
    pygame.quit()


if sys.platform != "emscripten":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Brainvita game (UI)")
    parser.add_argument(
        "--start-file",
        type=str,
        default=None,
        help="File containing the starting board state. If not provided, the default starting state is used.",
    )
    args = parser.parse_args()

    # asyncio is used to run the main function, for wasm compatibility
    if args.start_file:
        with open(args.start_file, "r") as f:
            asyncio.run(main(f.read()))
    else:
        asyncio.run(main())

else:
    # Wasm: No command line arguments
    asyncio.run(main())
