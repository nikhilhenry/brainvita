"""
Contains code to describe the current state of the game.
"""

from enum import Enum
from collections import defaultdict
from typing import Dict


class Position:
    def __init__(self, row: int, column: int):
        """
        Represent a location on the board
        """
        self.row = row
        self.column = column

    def __add__(self, other):
        row = self.row + other.row
        col = self.column + other.column
        return Position(row, col)

    def __sub__(self, other):
        row = self.row - other.row
        col = self.column - other.column
        return Position(row, col)

    def __hash__(self):
        return hash((self.row, self.column))

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __str__(self):
        return f"({self.row},{self.column})"

    def __repr__(self):
        return f"({self.row},{self.column})"


class Move:
    """
    Represents an action taken on a marble
    """

    def __init__(self, src: Position, dest: Position):
        self.src = src
        self.dst = dest

    def get_in_between_pos(self) -> Position:
        """
        Returns the position between the src and destionation
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

    def __str__(self):
        s = ""
        for row in range(self._SIZE):
            for column in range(self._SIZE):
                s += self._board[Position(row, column)].value + " "

            s += "\n"

        return s

    def __getitem__(self, pos: Position):
        return self._board[pos]

    def __setitem__(self, pos: Position, value: NodeState):
        self._board[pos] = value

    def __lte__(self, other):
        return self.num_marbles <= other.num_marbles

    def solvable(self):
        """
        Returns True if current arrangment of marbles allows for some marbles to be eliminated, else False.
        """
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

    def make_move(self, move: Move):
        """
        Returns a new game state based on the move.
        If move is illegal will return None
        """
        src, dst = move.src, move.dst
        # checking if move is within the playable region
        if self[src] == NodeState.INVALID and self[dst] == NodeState.INVALID:
            return None
        # checking if move is valid: move can only by up,down,left,right in 2 steps diagonals are not allowed
        # check that dest is empty
        if self[dst] != NodeState.EMPTY:
            return None
        mag_row = abs(src.row - dst.row)
        mag_col = abs(src.column - dst.column)
        # check for diagonals
        if mag_row != 0 and mag_col != 0:
            return None
        # check that move is only two steps
        if not ((mag_row == 2 and mag_col == 0) or (mag_row == 0 and mag_col == 2)):
            return None

        # making a new board state
        new_board = Board()
        new_board._board = self._board
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

        return new_board

    def get_possible_move_locations(self, pos: Position) -> list[Position]:
        """
        Returns a list of possible move-to positions from the given position
        """
        positions = []
        for i in range(-2, 3, 2):
            if i == 0:
                continue

            if self[pos + Position(i, 0)] == NodeState.EMPTY:
                positions.append(pos + Position(i, 0))
            if self[pos + Position(0, i)] == NodeState.EMPTY:
                positions.append(pos + Position(0, i))

        return positions

    def move_gen(self):
        """
        Generates all possible moves from the current state, eliminating states which do not reach termination
        """

        boards = []  # keep track of all possible neigbouring states
        for row in range(self._SIZE):
            for column in range(self._SIZE):
                if self[Position(row, column)] == NodeState.FILLED:
                    current = Position(row, column)
                    possible_dests = self.get_possible_move_locations(
                        current
                    )  # get all possible moves for that marble
                    for dest in possible_dests:
                        # compute the next states, can return a maximum of 4 valid states
                        new_board = self.make_move(Move(current, dest))
                        # eliminating the states which do not respect the domain constraints
                        if (
                            new_board != None and new_board.solvable()
                        ):  # check that we can progress from this state
                            boards.append(new_board)

        return boards

    def goal_test(self):
        """
        Returns True if the game is over
        """
        return self.num_marbles == 1


"""
Driver Testing Code
"""
if __name__ == "__main__":
    board = Board()
    print(board)
    while True:
        if board == None:
            print("invalid move please play better")
            break
        print(board.solvable())
        src_x = int(input("Enter src row: "))
        src_y = int(input("Enter src column: "))
        dst_x = int(input("Enter dst row: "))
        dst_y = int(input("Enter dst column: "))
        move = Move(Position(src_x, src_y), Position(dst_x, dst_y))
        board = board.make_move(move)
