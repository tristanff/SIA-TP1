import sokoban
import time
import matplotlib.pyplot as plt


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


# Call DFS-function for each level
def main():
    # Levels to load
    levels = {'1': [sokoban.initial_state_level1, sokoban.goal_state_level1],
              '2': [sokoban.initial_state_level2, sokoban.goal_state_level2],
              '3': [sokoban.initial_state_level3, sokoban.goal_state_level3]}

    dfs_data = {}

    for level, (initial_state, goal_state) in levels.items():
        solution, expanded_nodes, frontier_nodes, time_taken = dfs_search(initial_state, goal_state)
        dfs_data[level] = {'solution': solution, 'expanded_nodes': expanded_nodes, 'frontier_nodes': frontier_nodes,
                           'time_taken': time_taken}

    # Plot data for each level
    for level, data in dfs_data.items():
        print(f"Level {level}:")
        if data['solution']:
            print("Solution found! Time taken: {:.2f} seconds".format(data['time_taken']))
            print("Total amount of steps: ", len(data['solution']))
            print("Expanded nodes:", data['expanded_nodes'])
            print("Frontier nodes:", data['frontier_nodes'])
            # Plot the data
            plt.plot(level, data['time_taken'], marker='o', label=f'Level {level}')
        else:
            print("No solution found.")

    plt.figure(figsize=(10, 6))
    for level, data in dfs_data.items():
        if data['solution']:
            plt.plot(level, data['time_taken'], marker='o', label=f'Level {level} - DFS')
        else:
            plt.plot(level, 0, marker='o', label=f'Level {level} - DFS (No solution)')

    # Customize plot
    plt.xlabel('Level')
    plt.ylabel('Time taken (seconds)')
    plt.title('DFS Time Taken for Each Level')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()


if __name__ == "__main__":
    main()
