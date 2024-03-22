import time
from sokoban import initial_state, goal_test, generate_next_states, print_state

def bfs_solve(initial_state):
    # Initialize the frontier with the initial state
    frontier = [initial_state]
    # Initialize an empty set to keep track of visited states
    visited = set()
    # Initialize a dictionary to keep track of the path to each state
    parent = {str(initial_state): None}
    expanded_nodes = 0  # Counter for expanded nodes
    frontier_nodes = 1  # Counter for nodes in the frontier (initial state is in the frontier)

    # Continue searching until the frontier is empty
    while frontier:
        # Pop the first state from the frontier
        current_state = frontier.pop(0)
        # Increment the count of expanded nodes
        expanded_nodes += 1

        # Check if the current state is the goal state
        if goal_test(current_state):
            # Return the path to the goal state along with statistics
            return reconstruct_path(parent, current_state), expanded_nodes, frontier_nodes
        
        # Mark the current state as visited
        visited.add(str(current_state))

        # Generate all possible next states
        for next_state in generate_next_states(current_state):
            # Check if the next state has not been visited
            if str(next_state) not in visited:
                # Add the next state to the frontier
                frontier.append(next_state)
                # Increment the count of frontier nodes
                frontier_nodes += 1
                # Record the path to the next state
                parent[str(next_state)] = current_state

    # If no solution is found, return None along with statistics
    return None, expanded_nodes, frontier_nodes

def reconstruct_path(parent, state):
    # Reconstruct the path from the initial state to the given state
    path = []
    while state is not None:
        path.append(state)
        state = parent[str(state)]
    # Reverse the path to get the correct order
    path.reverse()
    return path

def main():
    # Measure the start time
    start_time = time.time()
    # Perform BFS search
    solution, expanded_nodes, frontier_nodes = bfs_solve(initial_state)
    # Measure the end time
    end_time = time.time()
    # Calculate the total time taken
    total_time = end_time - start_time

    # Print the solution if found
    if solution:
        print("Solution found!")
        print(f"Total number of steps: {len(solution) - 1}") # print total steps -1 since initial state doesn't count
        print(f"Total time to find the solution: {total_time} seconds")
        print(f"Expanded nodes: {expanded_nodes}")
        print(f"Frontier nodes: {frontier_nodes}")
        # print the board state of each step
        for i, state in enumerate(solution):
            print(f"Step {i}:") # starts at step 0 (initial state)
            print_state(state) 
            print()
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
