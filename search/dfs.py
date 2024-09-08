import copy
import time
from search._node import Node


def dhokla_first_search(start_node: Node):
    prev_marble_count = start_node.board.num_marbles

    open: list[Node] = [start_node]
    open_set = set([start_node.board])
    closed: set = set()

    while open != []:
        parent = open.pop()
        open_set.discard(parent.board)
        if parent.board.goal_test():
            return parent.back_track()
        else:
            if prev_marble_count > parent.board.num_marbles:
                prev_marble_count = parent.board.num_marbles
                print(f"Marbles left: {parent.board.num_marbles}")

            closed.add(parent.board)
            children: list = parent.board.move_gen()

            children = [
                child
                for child in children
                if child not in closed and child not in open_set
            ]

            # children = [child for child in children if child not in [op.board for op in open]]

            for child in children:
                open_set.add(child)
                open.append(Node(child, parent))

    return None


def stepped_dhokla_first_search(
    node: Node, open: list[Node] | None, open_set: set | None, closed: set
):

    if open is None and open_set is None:
        open_set = set([node.board])
        open = [node]

    parent = open.pop()
    open_set.discard(parent.board)

    if parent.board.goal_test():
        return True, parent, open, open_set, closed
    else:

        closed.add(parent.board)
        children: list = parent.board.move_gen()

        children = [
            child for child in children if child not in closed and child not in open_set
        ]

        for child in children:
            open.append(Node(child, parent))
            open_set.add(child)

        return False, parent, open, open_set, closed
