import sokoban
import time


# Define DFS-search function
def dfs_search(initial_state, goal_state):
    start_time = time.time()  # Start-time of DFS
    stack = [(initial_state, [])]  # Stack to store states and their corresponding actions
    visited = set()  # Set to keep track of visited states
    expanded_nodes = 0  # Counter for expanded nodes
    frontier_nodes = 1  # Counter for nodes in the frontier

    while stack:
        current_state, actions = stack.pop()  # Get the current state and its actions
        expanded_nodes += 1  # Adding expanded nodes
        if current_state == goal_state:  # Check if the current state is the goal state
            end_time = time.time()  # End-time of DFS
            return actions, expanded_nodes, frontier_nodes, end_time - start_time  # Return action that lead to the goal

        visited.add(tuple(map(tuple, current_state)))  # Mark the current state as visited

        # Generate next states and add them to the stack if they haven't been visited
        for next_state in sokoban.generate_next_states(current_state):
            if tuple(map(tuple, next_state)) not in visited:  # Convert state to a tuple, check if it has been visited
                stack.append((next_state, actions + [next_state]))  # Add the next state and actions to the stack
                frontier_nodes += 1  # Adding frontier nodes
    return None, frontier_nodes, expanded_nodes  # If no solution is found, return None + stats


# Define DFS-print function
def dfs_print(solution, expanded_nodes, frontier_nodes, time_taken):
    if solution:
        print("Solution found! Time taken: {:.2f} seconds".format(time_taken))  # Print the solution and time
        print("Total amount of steps: ", len(solution))  # Print steps taken
        print("Expanded nodes:", expanded_nodes)  # Print the number of expanded nodes
        print("Frontier nodes:", frontier_nodes)  # Print the number of nodes in the frontier

        for i, state in enumerate(solution):  # Print step-by-step to solution
            print(f"Step {i + 1}:")  # Print which step on
            sokoban.print_state(state)
            print()  # Print the current board
    else:
        print("No solution found.")  # Print if no solution is found


# Call DFS-function
def main():
    solution, expanded_nodes, frontier_nodes, time_taken = dfs_search(sokoban.initial_state, sokoban.goal_state)
    dfs_print(solution, expanded_nodes, frontier_nodes, time_taken)


if __name__ == "__main__":
    main()
