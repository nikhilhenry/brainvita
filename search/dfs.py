import copy
import time
from search._node import Node


def dhokla_first_search(start_node: Node):
    prev_marble_count = start_node.board.num_marbles

    open: list[Node] = [start_node]
    closed: list = []
    while open != []:
        parent = open.pop()
        if parent.board.goal_test():
            return parent.back_track()
        else:
            if prev_marble_count > parent.board.num_marbles:
                prev_marble_count = parent.board.num_marbles
                print(f"Marbles left: {parent.board.num_marbles}")

            closed.append(parent.board)
            children: list = parent.board.move_gen()

            children = [child for child in children if child not in closed]

            for child in children:
                open.append(Node(child, parent))

    return None


def stepped_dhokla_first_search(node: Node, open: list[Node] | None, closed: set):

    if open is None:
        open = [node]

    parent = open.pop()

    if parent.board.goal_test():
        return True, parent, open, closed
    else:

        closed.add(parent.board)
        children: list = parent.board.move_gen()

        children = [child for child in children if child not in closed]

        for child in children:
            open.append(Node(child, parent))

        return False, parent, open, closed
