"""
Contains code to describe the current state of the game.
"""

from enum import Enum


class NodeState(Enum):
    """
    Describes possible states a node on the board can take
    """

    FILLED = "x"
    EMPTY = "o"
    INVALID = "."

    def __str__(self):
        return self.value


class Board:
    """
    Defines the current board state, next possible moves, can also execute a move
    """

    def __init__(self):
        # board is a 7x7 matrix of states
        self.SIZE = 7
        self._board = [
            [NodeState.INVALID for _ in range(self.SIZE)] for _ in range(self.SIZE)
        ]
        self.num_marbles = 32
        # setup up valid square grids
        # top sub grid
        for row in range(2):
            for column in range(self.SIZE):
                if column > 1 and column < 5:
                    self._board[row][column] = NodeState.FILLED

        # middle sub grids
        for row in range(2, 5):
            for column in range(self.SIZE):
                self._board[row][column] = NodeState.FILLED

        # leave the middle empty
        self._board[3][3] = NodeState.EMPTY

        # top sub grid
        for row in range(5, self.SIZE):
            for column in range(self.SIZE):
                if column > 1 and column < 5:
                    self._board[row][column] = NodeState.FILLED

    def __str__(self):
        # @todo make the column spacing same as row spacing
        return "\n\n".join(
            ["  ".join([str(cell) for cell in row]) for row in self._board]
        )


"""
Driver Testing Code
"""

if __name__ == "__main__":
    board = Board()
    print(board)
