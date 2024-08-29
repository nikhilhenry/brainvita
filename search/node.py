from ..board import Board
class Node:
    """
    A wrapper class to represent a state and keep track of its parent
    """
    def __init__(self,board:Board,parent:Board | None = None):
        self.board = board
        self.parent = parent

    def __le__(self,other):
        return self.board.num_marbles < other.board.num_marbles

    def back_track(self):
        """
        Traverse parents and returns a list of all ancestor including current node
        """
        pass

