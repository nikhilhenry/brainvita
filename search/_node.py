from typing import Self


class Node:
    """
    A wrapper class to represent a state and keep track of its parent
    """

    def __init__(self, board, parent: Self | None = None):
        self.board = board
        self.parent = parent

    def __lt__(self, other: Self):
        return self.board < other.board

    def back_track(self, sequence=[]):
        """
        Traverse parents and returns a list of all ancestor including current node
        """
        sequence = sequence[:]
        if self.parent == None:
            sequence.append(self.board)
            return sequence

        sequence.append(self.board)
        return self.parent.back_track(sequence)
