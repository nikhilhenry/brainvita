from typing import Deque
from collections import deque
from search.node import Node

def bread_first_search(start_node:Node):
    count = 0
    # keep track of all the visited states ie Board
    closed = set()
    # queue to store all the states that haven't been visited
    open = deque()
    open.append(start_node)
    while len(open) != 0:
        # remove from the head
        parent = open.popleft()
        #print(f"Iter: {count}")
        #print(parent.board)
        #count += 1
        if parent.board.goal_test() == True:
            return parent.back_track()
        else:
            closed.add(parent.board)
            try:
                children = parent.board.move_gen()
                # removing already visited states
                children = [child for child in children if child not in closed]
                for child in children:
                    open.append(Node(child,parent))
            except:
                print("failed weired")
                path = parent.back_track()
                for p in path[::-1]:
                    print(p)


