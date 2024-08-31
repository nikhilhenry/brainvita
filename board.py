"""
Contains code to describe the current state of the game.
"""

from __future__ import annotations

from enum import Enum
from collections import defaultdict
import pickle
from typing import Dict
from search import dhokla_first_search, best_first_search, bread_first_search
from utils import Position
from search import Node
import copy
import time

import argparse


class Move:
    """
    Represents an action taken on a marble
    """

    def __init__(self, src: Position, dest: Position):
        self.src = src
        self.dst = dest

    def get_in_between_pos(self) -> Position:
        """
        Returns the position between the src and destination
        """
        dir = self.dst - self.src
        dir.row //= 2
        dir.column //= 2
        return self.src + dir


class NodeState(Enum):
    """
    Describes possible states a node on the board can take
    """

    FILLED = "x"
    EMPTY = "o"
    INVALID = "."

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class Board:
    """
    Defines the current board state, next possible moves, can also execute a move
    """

    def __init__(self):

        self._SIZE = 7

        # state
        self.num_marbles = 32
        self._board: Dict[Position, NodeState] = defaultdict(lambda: NodeState.INVALID)

        # Initialize the starting grid

        # top sub grid
        for row in range(2):
            for column in range(self._SIZE):
                if column > 1 and column < 5:
                    self._board[Position(row, column)] = NodeState.FILLED

        # middle sub grids
        for row in range(2, 5):
            for column in range(self._SIZE):
                self._board[Position(row, column)] = NodeState.FILLED

        # leave the middle empty
        self._board[Position(3, 3)] = NodeState.EMPTY

        # top sub grid
        for row in range(5, self._SIZE):
            for column in range(self._SIZE):
                if column > 1 and column < 5:
                    self._board[Position(row, column)] = NodeState.FILLED

    @classmethod
    def construct_from_string(cls, s: str):
        """
        Construct a board from a string representation
        """
        s = s.replace("\n", "").replace(" ", "")
        new_board = cls()
        new_board.num_marbles = 0
        for row in range(new_board._SIZE):
            for column in range(new_board._SIZE):
                new_board._board[Position(row, column)] = NodeState(
                    s[row * new_board._SIZE + column]
                )
                if new_board._board[Position(row, column)] == NodeState.FILLED:
                    new_board.num_marbles += 1

        return new_board

    def __hash__(self) -> int:
        # to allow for hashing of the board state, we use the string representation
        return hash(str(self))

    def __str__(self) -> str:
        s = ""
        for row in range(self._SIZE):
            for column in range(self._SIZE):
                s += self._board[Position(row, column)].value + " "

            s += "\n"
        s += f"MARBLES: {self.num_marbles}\n"
        return s

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, pos: Position) -> NodeState:
        return self._board[pos]

    def __setitem__(self, pos: Position, value: NodeState):
        self._board[pos] = value

    def __le__(self, other):
        return self.num_marbles <= other.num_marbles

    def __eq__(self, other):
        return hash(self) == hash(other)

    def solvable(self) -> bool:
        """
        Returns True if current arrangment of marbles allows for some marbles to be eliminated, else False.
        """
        if self.num_marbles == 1:
            # solved!
            return True

        if self.num_marbles > 4:
            # some moves can still be made in this state
            return True

        marble_positions = [
            pos for pos, state in self._board.items() if state == NodeState.FILLED
        ]
        # compute the distance between this marble and every other marble
        for marble in marble_positions:
            for other in marble_positions:
                if other == marble:
                    continue
                distance = marble - other
                # if either difference in column or row is odd we can eliminate a marble
                if distance.row == 0 and distance.column % 2 == 1:
                    return True
                if distance.column == 0 and distance.row % 2 == 1:
                    return True
        return False

    def make_move(self, move: Move) -> Board | None:
        """
        Returns a new game state (Board) based on the move.
        If move is illegal will return None.
        """
        src, dst = move.src, move.dst

        # region: check if the move is valid

        # checking if move is within the playable region
        if self[src] == NodeState.INVALID and self[dst] == NodeState.INVALID:
            return None

        # check that dest is empty
        if self[dst] != NodeState.EMPTY:
            return None

        mag_row = abs(src.row - dst.row)
        mag_col = abs(src.column - dst.column)

        # check for diagonals - diagnols are not allowed
        if mag_row != 0 and mag_col != 0:
            return None

        # check that move is only two steps (move can only by up,down,left,right in 2 steps. )
        if not ((mag_row == 2 and mag_col == 0) or (mag_row == 0 and mag_col == 2)):
            return None

        # check that dst is present within the bounds
        if dst.row >= self._SIZE or dst.column >= self._SIZE:
            return None
        if dst.row < 0 or dst.column < 0:
            return None

        # endregion

        # region: making a new board state

        new_board = Board()
        new_board._board = copy.deepcopy(self._board)
        new_board.num_marbles = self.num_marbles

        # removing the marble from current pos
        new_board[src] = NodeState.EMPTY
        # setting the marble to the dest position
        new_board[dst] = NodeState.FILLED

        # remove a marble if present in between path
        in_between_pos = move.get_in_between_pos()
        if new_board[in_between_pos] == NodeState.FILLED:
            new_board[in_between_pos] = NodeState.EMPTY
            new_board.num_marbles -= 1

        # endregion

        return new_board

    def get_possible_move_locations(self, pos: Position) -> list[Position]:
        """
        Returns a list of possible move-to positions from the given position
        """
        positions = []
        for i in range(-2, 3, 2):
            if i == 0:  # to avoid self moves
                continue

            if self[pos + Position(i, 0)] == NodeState.EMPTY:
                positions.append(pos + Position(i, 0))
            if self[pos + Position(0, i)] == NodeState.EMPTY:
                positions.append(pos + Position(0, i))

        return positions

    def move_gen(self) -> list[Board]:
        """
        Generates all possible moves from the current state, eliminating states which do not reach termination
        """

        boards: list[Board] = []

        for row in range(self._SIZE):
            for column in range(self._SIZE):
                if self[Position(row, column)] == NodeState.FILLED:

                    current = Position(row, column)

                    # get all possible moves for that marble
                    possible_dests = self.get_possible_move_locations(current)
                    for dest in possible_dests:
                        # compute the next states, can return a maximum of 4 valid states
                        new_board = self.make_move(Move(current, dest))
                        # if the move is invalid, or leads to a state where no more moves can be made, skip
                        if new_board is None or not new_board.solvable():
                            continue

                        boards.append(new_board)

        return boards

    def goal_test(self) -> bool:
        """
        Returns True if the game is over
        """
        return self.num_marbles == 1


"""
CLI interface for the game
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brainvita game (CLI)")
    parser.add_argument(
        "--start-file",
        type=str,
        default=None,
        help="File containing the starting board state. If not provided, the default starting state is used.",
    )
    parser.add_argument(
        "--solver",
        type=str,
        default="best",
        choices=["bfs", "dfs", "best", "manual"],
        help="Solver to use. Options: bfs, dfs, best, manual. Default: best",
    )
    parser.add_argument(
        "--savefile",
        type=str,
        default="sequence.pkl",
        help="Filename to save the sequence of moves. Default: sequence.pkl",
    )
    args = parser.parse_args()

    if args.start_file:
        with open(args.start_file, "r") as f:
            board = Board.construct_from_string(f.read())
    else:
        board = Board()

    print("STARTING STATE")
    print(board)

    start_node = Node(board)
    st = time.time()
    if args.solver == "bfs":
        print("Using Breadth First Search")
        sequence = bread_first_search(start_node)
    elif args.solver == "dfs":
        print("Using Depth First Search")
        sequence = dhokla_first_search(start_node)
    elif args.solver == "best":
        print("Using Best First Search")
        sequence = best_first_search(start_node)
    else:
        sequence = [board]
        old_board = None
        while True:
            print(board)
            src_x = int(input("Enter src row: "))
            src_y = int(input("Enter src col: "))
            dst_x = int(input("Enter dst row: "))
            dst_y = int(input("Enter dst col: "))
            move = Move(Position(src_x, src_y), Position(dst_x, dst_y))
            old_board = board
            board = board.make_move(move)
            if board is None:
                print("Invalid Move!")
                board = old_board
            else:
                sequence.append(board)
                if board.goal_test():
                    print("Game Over! You won!")
                    break
                elif not board.solvable():
                    print(
                        "Game Over - No more moves can be made! Better luck next time."
                    )
                    break

        sequence = sequence[::-1]  # store in reverse order

    print(f"Time taken: {round(time.time() - st,3)}s | Steps taken: {len(sequence)}")
    pickle.dump([str(board) for board in sequence], open(args.savefile, "wb"))

    print(f"(Reverse) Sequence of moves saved to {args.savefile}.")
