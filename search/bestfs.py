from search._node import Node
import heapq


def best_first_search(start_node: Node):
    prev_marble_count = start_node.board.num_marbles

    # keep track of all the visited states ie Board
    closed = set()
    # queue to store all the states that haven't been visited
    open = []
    heapq.heappush(open, start_node)
    while len(open) != 0:
        parent = heapq.heappop(open)
        # remove from the head
        if parent.board.goal_test() == True:
            return parent.back_track()
        else:
            if prev_marble_count > parent.board.num_marbles:
                prev_marble_count = parent.board.num_marbles
                print(f"Marbles left: {parent.board.num_marbles}")

            closed.add(parent.board)
            children = parent.board.move_gen()
            # removing already visited states
            children = [child for child in children if child not in closed]
            # if parent.board.num_marbles == 2:
            #     print(f"FROM\n{parent.board}")
            for child in children:
                # if parent.board.num_marbles == 2:
                #     print(f"POSSIBLE\n{child}")
                heapq.heappush(open, Node(child, parent))
            # if len(children) != 0:
            #     print("=====")

    return None
