import asyncio
import enum
import time
import pygame
import constants as c
from board import Board, Move, NodeState
from music_controller import MusicController
import sys
import platform
from search import (
    Node,
    stepped_dhokla_first_search,
    stepped_best_first_search,
    stepped_bread_first_search,
)
import argparse

import widgets
from sprites import Marble

# initialize pygame
pygame.init()


class GameState(enum.Enum):
    """
    An enum to represent the game state, for animation and showing the game over screen.
    """

    MANUAL = 0  # default game state is manual
    ANIMATING = 1
    LOST = 2
    WIN = 3


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

        self.game_state = GameState.MANUAL
        self.algorithm = None
        self.autovars_open = None
        self.autovars_closed = set()
        self.autostats = {
            "start_time": 0,
            "end_time": 0,
            "steps": 0,
        }
        self.move_count = 0
        self.is_game_over = False
        self.selected_marble = None
        self.possible_positions = []
        self.undo_stack = []

        # musician
        self.musician = musician
        self.musician.start()

        # Create the marble sprites
        self.marble_list = pygame.sprite.Group()
        for pos in self.board._board:
            marble = Marble(pos, state=self.board._board[pos])
            self.marble_list.add(marble)

        # Create the buttons
        self.dfs_button = widgets.ImageButton(
            (30, 200),
            c.SPRT_DFS_BTN,
            hovered_surface=c.SPRT_DFS_BTN_CLICKED,
            clicked_surface=c.SPRT_DFS_BTN_CLICKED,
        )
        self.bfs_button = widgets.ImageButton(
            (30, 200 + 60),
            c.SPRT_BFS_BTN,
            hovered_surface=c.SPRT_BFS_BTN_CLICKED,
            clicked_surface=c.SPRT_BFS_BTN_CLICKED,
        )
        self.bestfs_button = widgets.ImageButton(
            (30, 260 + 60),
            c.SPRT_BESTFS_BTN,
            hovered_surface=c.SPRT_BESTFS_BTN_CLICKED,
            clicked_surface=c.SPRT_BESTFS_BTN_CLICKED,
        )

        self.reset_button = widgets.ImageButton(
            (30, 400),
            c.SPRT_RESTART_BTN,
            hovered_surface=c.SPRT_RESTART_BTN_CLICKED,
            clicked_surface=c.SPRT_RESTART_BTN_CLICKED,
        )
        self.mute_button = widgets.ImageToggleButton(
            (30 + 64 + 5, 400),
            c.SPRT_MUSIC_ON_BTN,
            c.SPRT_MUSIC_OFF_BTN,
            c.SPRT_MUSIC_ON_BTN_HOVERED,
            c.SPRT_MUSIC_OFF_BTN_HOVERED,
        )
        self.undo_button = widgets.ImageButton(
            (99 + 64 + 5, 400),
            c.SPRT_UNDO_BTN,
            hovered_surface=c.SPRT_UNDO_BTN_CLICKED,
            clicked_surface=c.SPRT_UNDO_BTN_CLICKED,
        )

        self.button_list = pygame.sprite.Group(
            self.reset_button,
            self.dfs_button,
            self.bfs_button,
            self.bestfs_button,
            self.mute_button,
            self.undo_button,
        )

    def reset_base(self):
        self.board = Board()
        self.move_count = 0
        self.game_state = GameState.MANUAL
        self.algorithm = None
        self.autovars_closed = set()
        self.autovars_open = None
        self.autostats = {
            "start_time": 0,
            "end_time": 0,
            "steps": 0,
        }

        self.update_marble_state()
        self.selected_marble = None
        self.possible_positions = []
        self.undo_stack = []

    def update_marble_state(self):
        """
        Update the marble states based on the board state
        """
        for marble in self.marble_list:
            marble.update(marble.pos, self.board[marble.pos])

    def process_events(self) -> None:
        """
        Process all events. This includes mouse clicks, button clicks, etc.
        This shouldn't contain logic, but it should call the appropriate methods.
        It should update the game state based on the events.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_over = True
            if event.type == pygame.MOUSEMOTION:
                # update button hover state
                for button in self.button_list:
                    button.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GameState.MANUAL:
                    # get which marble is hovered and clicked (if any)
                    for marble in self.marble_list:
                        if marble.rect.collidepoint(event.pos):
                            # mark marble as selected, prompting move generation for that marble
                            self.selected_marble = marble
                            self.musician.play_select_sound()

                    # get which possible move is clicked (if any)
                    for move in self.possible_positions:
                        if (
                            c.POS2COORD[move].x
                            < event.pos[0]
                            < c.POS2COORD[move].x
                            + 18 * c.SCALE_FACTOR  # 18 is the width of the marble
                        ):
                            if (
                                c.POS2COORD[move].y
                                < event.pos[1]
                                < c.POS2COORD[move].y
                                + 18 * c.SCALE_FACTOR  # 18 is the height of the marble
                            ):
                                # move the marble
                                new_board = self.board.make_move(
                                    Move(self.selected_marble.pos, move)
                                )
                                if new_board:
                                    self.undo_stack.append(self.board)
                                    self.musician.play_move_sound()
                                    self.board = new_board
                                    self.move_count += 1
                                    self.update_marble_state()
                                    self.selected_marble = None
                                    self.possible_positions = []
                                    if self.board.goal_test():
                                        self.game_state = GameState.WIN
                                    elif not self.board.solvable():
                                        self.game_state = GameState.LOST

                # get which button is clicked (if any)
                button: widgets.ImageButton | widgets.ImageToggleButton
                for button in self.button_list:
                    if button.hovered:
                        button.click()

    def main_logic(self):
        """
        Main game logic loop for Brainvita.
        """

        # Button logic
        if self.reset_button.is_clicked:
            self.reset_base()
            self.reset_button.unclick()
        elif self.dfs_button.is_clicked:
            if self.game_state != GameState.ANIMATING:
                self.game_state = GameState.ANIMATING
                self.algorithm = "dfs"
                self.autostats["start_time"] = time.time()
            self.dfs_button.unclick()
        elif self.bfs_button.is_clicked:
            if self.game_state != GameState.ANIMATING:
                self.game_state = GameState.ANIMATING
                self.algorithm = "bfs"
                self.autostats["start_time"] = time.time()
            self.bfs_button.unclick()
        elif self.bestfs_button.is_clicked:
            if self.game_state != GameState.ANIMATING:
                self.game_state = GameState.ANIMATING
                self.algorithm = "bestfs"
                self.autostats["start_time"] = time.time()
            self.bestfs_button.unclick()
        elif self.undo_button.is_clicked:
            if self.game_state == GameState.MANUAL and len(self.undo_stack) > 0:
                self.board = self.undo_stack.pop()
                self.move_count += 1  # undoing a move is also a move
                self.update_marble_state()
            self.undo_button.unclick()

        if self.mute_button.is_toggled:
            self.musician.mute()
        else:
            if not self.musician.is_playing:
                self.musician.unmute()

        # Game logic
        if self.game_state == GameState.MANUAL:
            if self.selected_marble:
                move_locations = self.board.get_possible_move_locations(
                    self.selected_marble.pos
                )
                self.possible_positions = move_locations
        elif self.game_state == GameState.ANIMATING:
            if self.algorithm == "dfs":
                function = stepped_dhokla_first_search
            elif self.algorithm == "bfs":
                function = stepped_bread_first_search
            elif self.algorithm == "bestfs":
                function = stepped_best_first_search

            game_over, board_node, self.autovars_open, self.autovars_closed = function(
                Node(self.board), self.autovars_open, self.autovars_closed
            )
            self.board = board_node.board
            self.autostats["steps"] = len(board_node.back_track())
            self.autostats["end_time"] = time.time()
            self.update_marble_state()
            self.move_count += 1

            if game_over:
                self.game_state = GameState.WIN

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
        rendered_text = c.FONT_UI_MONO.render(
            f"{'Moves:':<10}{self.move_count:>6}", False, (0, 0, 0)
        )
        c.ROOT_DISPLAY.blit(rendered_text, (30, 120))

        rendered_text = c.FONT_UI_MONO.render(
            f"{'Marbles:':<10}{self.board.num_marbles:>6}", False, (0, 0, 0)
        )
        c.ROOT_DISPLAY.blit(rendered_text, (30, 150))

        self.marble_list.draw(c.ROOT_DISPLAY)

        if self.game_state == GameState.MANUAL:

            if self.selected_marble:
                c.ROOT_DISPLAY.blit(
                    c.SPRT_SELECTED_MARBLE,
                    (self.selected_marble.rect.x, self.selected_marble.rect.y),
                )
            if self.possible_positions:
                for move in self.possible_positions:
                    c.ROOT_DISPLAY.blit(
                        c.SPRT_POSSIBLE_MOVE,
                        (c.POS2COORD[move].x, c.POS2COORD[move].y),
                    )
        elif self.game_state == GameState.ANIMATING:

            rendered_text = c.FONT_MAIN.render(
                f"{f'{self.algorithm} ON':>30}", False, (26, 150, 28)
            )
            c.ROOT_DISPLAY.blit(rendered_text, (350, 50))

            # render algorithm statistics

        elif self.game_state == GameState.WIN:

            rendered_text = c.FONT_MAIN.render("WIN!", False, (26, 150, 28))
            c.ROOT_DISPLAY.blit(rendered_text, (990, 50))

            marble: Marble
            for marble in self.marble_list:
                if self.board[marble.pos] != NodeState.EMPTY:
                    c.ROOT_DISPLAY.blit(
                        c.SPRT_MARBLE_WIN,
                        (marble.rect.x, marble.rect.y),
                    )

            rendered_text = c.FONT_UI_MONO.render(
                f"{'Time:':<8}{round(self.autostats['end_time']-self.autostats['start_time'], 2):>6}s",
                False,
                (0, 0, 0),
            )
            c.ROOT_DISPLAY.blit(rendered_text, (1000, 120))
            rendered_text = c.FONT_UI_MONO.render(
                f"{'PathLen:':<8}{self.autostats['steps']:>7}", False, (0, 0, 0)
            )
            c.ROOT_DISPLAY.blit(rendered_text, (1000, 150))

        elif self.game_state == GameState.LOST:

            rendered_text = c.FONT_MAIN.render("LOST!", False, (184, 33, 33))
            c.ROOT_DISPLAY.blit(rendered_text, (990, 50))

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
        game.main_logic()
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
