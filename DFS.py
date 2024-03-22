import sokoban
from time import time


#Define the DFS function
def dfs_search(initial_state, goal_state):
    start = time() # Start-time of DFS
    stack = [(initial_state, [])]  # Stack to store states and their corresponding actions
    visited = set()  # Set to keep track of visited states
    expanded_nodes = 0  # Counter for expanded nodes
    frontier_nodes = 0  # Counter for nodes in the frontier

    while stack:
        current_state, actions = stack.pop()  # Get the current state and its actions
        expanded_nodes += 1 # Adding expanded nodes
        if current_state == goal_state:  # Check if the current state is the goal state
            end = time() # End-time of DFS
            return actions, expanded_nodes, frontier_nodes, end - start  # Return the actions that lead to the goal state

        visited.add(tuple(map(tuple, current_state)))  # Mark the current state as visited

        # Generate next states and add them to the stack if they haven't been visited
        for next_state in sokoban.generate_next_states(current_state):
            if tuple(map(tuple, next_state)) not in visited: # Convert state to a tuple, check if it has/not been visited
                stack.append((next_state, actions + [next_state]))  # Add the next state and actions to the stack
                frontier_nodes += 1 # Adding frontier nodes
    return None  # If no solution is found, return None


# Perform DFS search
solution, expanded_nodes, frontier_nodes, time_taken = dfs_search(sokoban.initial_state, sokoban.goal_state)

# Print solution if found
if solution:
    print("Solution found! time taken: ", time_taken, "seconds") # Prin the solution and time
    print("total amount of steps: ", len(solution)) # Print steps taken
    print("Expanded nodes:", expanded_nodes)  # Print the number of expanded nodes
    print("Frontier nodes:", frontier_nodes)  # Print the number of nodes in the frontier

    for i, state in enumerate(solution): #Print step by step to solution
        print(f"Step {i + 1}:") # Print which step on
        sokoban.print_state(state)
        print() # Print the current board



else:
    print("No solution found.") # Print if no solution is find