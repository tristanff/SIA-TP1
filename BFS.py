import time
import matplotlib.pyplot as plt
import sokoban

def bfs_solve(initial_state, goal_state):
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
        if sokoban.goal_test(current_state, goal_state):
            # Return the path to the goal state along with statistics
            return reconstruct_path(parent, current_state), expanded_nodes, frontier_nodes

        # Mark the current state as visited
        visited.add(tuple(map(tuple, current_state)))

        # Generate all possible next states
        for next_state in sokoban.generate_next_states(current_state):
            # Check if the next state has not been visited
            if tuple(map(tuple, next_state)) not in visited:
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
    levels = {'1': [sokoban.initial_state_level1, sokoban.goal_state_level1],
              '2': [sokoban.initial_state_level2, sokoban.goal_state_level2],
              '3': [sokoban.initial_state_level3, sokoban.goal_state_level3]}

    bfs_data = {}
    for level, (initial_state, goal_state) in levels.items():
        # Measure the start time
        start_time = time.time()
        # Perform BFS search
        solution, expanded_nodes, frontier_nodes = bfs_solve(initial_state, goal_state)
        # Measure the end time
        end_time = time.time()
        # Calculate the total time taken
        total_time = end_time - start_time
        bfs_data[level] = {'solution': solution, 'expanded_nodes': expanded_nodes, 'frontier_nodes': frontier_nodes, 'time_taken': total_time}

        # Print the solution if found
        if solution:
            print("Solution found!")
            print(f"Total number of steps: {len(solution) - 1}")  # print total steps -1 since initial state doesn't count
            print("Total time to find the solution: {:.2f} seconds".format(total_time))
            print(f"Expanded nodes: {expanded_nodes}")
            print(f"Frontier nodes: {frontier_nodes}")
            # Print the board state of each step
            for i, state in enumerate(solution):
                print(f"Step {i + 1}:")  # starts at step 1 (initial state)
                sokoban.print_state(state)
                print()
        else:
            print("No solution found.")

    # Plotting BFS time taken for each level
    levels_list = []
    times_list = []
    for level, data in bfs_data.items():
        levels_list.append(level)
        times_list.append(data['time_taken'])

    plt.plot(levels_list, times_list, marker='o')
    plt.xlabel('Level')
    plt.ylabel('Time taken (seconds)')
    plt.title('BFS Time Taken for Each Level')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
