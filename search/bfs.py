from typing import Deque,Set
from collections import deque
from search.node import Node
from ..board import Board

def bread_first_search(start_node:Node):
    # keep track of all the visited states ie Board
    closed:Set[Board] = set()
    # queue to store all the states that haven't been visited
    open:Deque[Node] = deque()
    while len(open) != 0:
        parent = open.popleft() # remove from the head
        if parent.board.goal_test() == True:
            return parent.back_track()
        else:
            closed.add(parent.board)
            children = parent.board.move_gen()
            # removing already visited states
            children = [child for child in children if child not in closed]
            nodes = []
            for child in children:
                nodes.append(Node(child,parent.board))
            open.extend(nodes)

if __name__ == "__main__":
    board = Board()
    start_node = Node(board)
    sequence = bread_first_search(start_node)
    print(sequence)
