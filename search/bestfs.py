from search.node import Node
import heapq

def best_first_search(start_node:Node):
    # keep track of all the visited states ie Board
    closed = set()
    # queue to store all the states that haven't been visited
    open = []
    heapq.heappush(open,start_node)
    while len(open) != 0:
        parent = heapq.heappop(open)
        # remove from the head
        if parent.board.goal_test() == True:
            return parent.back_track()
        else:
            closed.add(parent.board)
            children = parent.board.move_gen()
            # removing already visited states
            children = [child for child in children if child not in closed]
            for child in children:
                heapq.heappush(open,Node(child,parent))

