import sys
from typing import Deque
from collections import deque
from search._node import Node


def bread_first_search(start_node: Node):
    prev_marble_count = start_node.board.num_marbles

    # keep track of all the visited states ie Board
    closed = set()
    # queue to store all the states that haven't been visited
    open = deque()
    open.append(start_node)
    while len(open) != 0:
        # remove from the head
        parent = open.popleft()
        # print(f"Iter: {count}")
        # print(parent.board)
        # count += 1
        if parent.board.goal_test() is True:
            return parent.back_track()
        else:
            if prev_marble_count > parent.board.num_marbles:
                prev_marble_count = parent.board.num_marbles
                print(f"Marbles left: {parent.board.num_marbles}")

            closed.add(parent.board)
            children = parent.board.move_gen()
            # removing already visited states
            children = [child for child in children if child not in closed]
            for child in children:
                open.append(Node(child, parent))


def stepped_bread_first_search(node: Node, open: Deque[Node] | None, closed: set):

    if open is None:
        open = deque()
        open.append(node)

    parent = open.popleft()

    if parent.board.goal_test():
        return True, parent, open, closed
    else:

        closed.add(parent.board)
        children: list = parent.board.move_gen()

        children = [child for child in children if child not in closed]

        for child in children:
            open.append(Node(child, parent))

        return False, parent, open, closed
