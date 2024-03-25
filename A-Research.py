# importer les fonctions nécessaires depuis game.py
from sokoban import *
import heapq
import time

# Define Manhattan distance heuristic function
def manhattan_distance(state,goal_state):
    distance = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '*':
                box_pos = (i, j)
                target_pos = None
                # Find the closest target position
                for x in range(len(goal_state)):
                    for y in range(len(goal_state[x])):
                        if goal_state[x][y] == '*':
                            target_pos = (x, y)
                            break
                    if target_pos:
                        break
                distance += abs(box_pos[0] - target_pos[0]) + abs(box_pos[1] - target_pos[1])
    return distance

# Define Misplaced Tiles heurisitic function
def misplaced_tiles(state,goal_state):
    heuristic = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != goal_state[i][j] and (state[i][j] != '#' or state[i][j] != '@'): # We don't care about final player Position
                heuristic += 1
    return heuristic

# Define Node class that will be used  for A* algorithm
class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g  # Cost from start node to current node
        self.h = h  # Heuristic cost from current node to goal node

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

# Define A* algorithm function
def astarMan(initial_state,goal_state):
    start_time = time.time()

    # Initialize start node
    start_node = Node(initial_state, g=0, h=manhattan_distance(initial_state,goal_state))

    # Initialize open and closed sets
    open_set = []
    closed_set = set()

    # Add start node to open set
    heapq.heappush(open_set, start_node)

    # Initialize statistics
    nodes_expanded = 0
    nodes_generated = 1  # Start node is generated

    # A* algorithm loop
    while open_set:
        # Pop node with lowest f=g+h value from open set
        current_node = heapq.heappop(open_set)

        # Check if current node is goal state
        if goal_test(current_node.state,goal_state):
            end_time = time.time()
            return {
                'State': 'Success',
                'Cost': current_node.g,
                'NodesExpanded': nodes_expanded,
                'FrontierNodes': len(open_set),
                'Solution': reconstruct_path(current_node),
                'ProcessTime': round(end_time - start_time, 2)
            }

        # Add current node to closed set
        closed_set.add(tuple(map(tuple, current_node.state)))

        # Generate next states
        next_states = generate_next_states(current_node.state)
        nodes_expanded += 1

        # Expand current node
        for next_state in next_states:
            # Create a new node for the next state
            next_node = Node(next_state, parent=current_node, action=None, g=current_node.g + 1,
                             h=manhattan_distance(next_state,goal_state))

            # Check if the next state is already visited or in the open set with lower cost
            if tuple(map(tuple, next_state)) in closed_set:
                continue

            # Add the next node to the open set
            heapq.heappush(open_set, next_node)
            nodes_generated += 1

        # If open set is empty and goal state not found, return failure
    end_time = time.time()
    return {
        'State': 'Failed',
        'Cost': None,
        'NodesExpanded': nodes_expanded,
        'FrontierNodes': len(open_set),
        'Solution': None,
        'ProcessTime': round(end_time - start_time, 2)
    }

def astarMisplaced(initial_state,goal_state):
    start_time = time.time()

    # Initialize start node
    start_node = Node(initial_state, g=0, h=misplaced_tiles(initial_state,goal_state))

    # Initialize open and closed sets
    open_set = []
    closed_set = set()

    # Add start node to open set
    heapq.heappush(open_set, start_node)

    # Initialize statistics
    nodes_expanded = 0
    nodes_generated = 1  # Start node is generated

    # A* algorithm loop
    while open_set:
        # Pop node with lowest f=g+h value from open set
        current_node = heapq.heappop(open_set)

        # Check if current node is goal state
        if goal_test(current_node.state, goal_state):
            end_time = time.time()
            return {
                'State': 'Success',
                'Cost': current_node.g,
                'NodesExpanded': nodes_expanded,
                'FrontierNodes': len(open_set),
                'Solution': reconstruct_path(current_node),
                'ProcessTime': round(end_time - start_time,2)
            }

        # Add current node to closed set
        closed_set.add(tuple(map(tuple, current_node.state)))

        # Generate next states
        next_states = generate_next_states(current_node.state)
        nodes_expanded += 1

        # Expand current node
        for next_state in next_states:
            # Create a new node for the next state
            next_node = Node(next_state, parent=current_node, action=None, g=current_node.g + 1,
                             h=misplaced_tiles(next_state,goal_state))

            # Check if the next state is already visited or in the open set with lower cost
            if tuple(map(tuple, next_state)) in closed_set:
                continue

            # Add the next node to the open set
            heapq.heappush(open_set, next_node)
            nodes_generated += 1

        # If open set is empty and goal state not found, return failure
    end_time = time.time()
    return {
        'State': 'Failed',
        'Cost': None,
        'NodesExpanded': nodes_expanded,
        'FrontierNodes': len(open_set),
        'Solution': None,
        'ProcessTime': round(end_time - start_time, 2)
    }

# Define function to reconstruct path from goal node to start node
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

# call the A* search algorithm
def main():
    # Run A* algorithm
    print("############# A* with MANHATTAN DISTANCE heuristic ################# \n")
    resultMan = astarMan(initial_state_level2,goal_state_level2)

    # Print results
    for key, value in resultMan.items():
        if(key != "Solution"):
            print(f"{key}: {value}")
    solucion = resultMan["Solution"]
    for i, steps in enumerate(solucion):
        print(f"Step {i + 1}:") # starts at step 0 (initial state)
        for line in steps:
            print(" ".join(line))

    print("############# A* with MISPLACED TILES heuristic ################# \n")
    resultMisp = astarMisplaced(initial_state_level2,goal_state_level2)

    for key, value in resultMisp.items():
        if (key != "Solution"):
            print(f"{key}: {value}")
    solucion = resultMisp["Solution"]
    for i, steps in enumerate(solucion):
        print(f"Step {i + 1}:")  # starts at step 0 (initial state)
        for line in steps:
            print(" ".join(line))

if __name__ == "__main__":
    main()
