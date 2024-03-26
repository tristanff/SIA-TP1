import matplotlib.pyplot as plt
from sokoban import *
from astar import *
import matplotlib.pyplot as plt
import numpy as np


def main():
    # Define the number of iterations to run for each level
    num_iterations = 5

    # Define the levels
    levels = [1, 2, 3]

    # Initialize empty lists to store the results
    manhattan_costs = [[] for _ in levels]
    manhattan_nodes_expanded = [[] for _ in levels]
    manhattan_frontier_nodes = [[] for _ in levels]
    manhattan_process_times = [[] for _ in levels]

    misplaced_costs = [[] for _ in levels]
    misplaced_nodes_expanded = [[] for _ in levels]
    misplaced_frontier_nodes = [[] for _ in levels]
    misplaced_process_times = [[] for _ in levels]

    # Loop through the levels and run the A* algorithm with both heuristics for multiple iterations
    for level in levels:
        for i in range(num_iterations):
            print(f"Running A* algorithm for level {level} iteration {i + 1}...")

            # Define the initial and goal states for the current level
            initial_state = eval(f"initial_state_level{level}")
            goal_state = eval(f"goal_state_level{level}")

            # Run A* algorithm with Manhattan Distance heuristic
            resultMan = astarMan(initial_state, goal_state)
            print(f"ResultMan :  {resultMan['Cost']}")

            # Store the results for the current iteration
            manhattan_costs[level - 1].append(resultMan['Cost'])
            manhattan_nodes_expanded[level - 1].append(resultMan['NodesExpanded'])
            manhattan_frontier_nodes[level - 1].append(resultMan['FrontierNodes'])
            manhattan_process_times[level - 1].append(resultMan['ProcessTime'])

            # Run A* algorithm with Misplaced Tiles heuristic
            resultMisp = astarMisplaced(initial_state, goal_state)
            print(f"ResultMisp :  {resultMisp['Cost']}")
            # Store the results for the current iteration
            misplaced_costs[level - 1].append(resultMisp['Cost'])
            misplaced_nodes_expanded[level - 1].append(resultMisp['NodesExpanded'])
            misplaced_frontier_nodes[level - 1].append(resultMisp['FrontierNodes'])
            misplaced_process_times[level - 1].append(resultMisp['ProcessTime'])

    # Calculate the average results for each level and heuristic
    manhattan_avg_costs = [sum(costs) / num_iterations for costs in manhattan_costs]
    manhattan_avg_nodes_expanded = [sum(nodes) / num_iterations for nodes in manhattan_nodes_expanded]
    manhattan_avg_frontier_nodes = [sum(nodes) / num_iterations for nodes in manhattan_frontier_nodes]
    manhattan_avg_process_times = [sum(times) / num_iterations for times in manhattan_process_times]

    misplaced_avg_costs = [sum(costs) / num_iterations for costs in misplaced_costs]
    misplaced_avg_nodes_expanded = [sum(nodes) / num_iterations for nodes in misplaced_nodes_expanded]
    misplaced_avg_frontier_nodes = [sum(nodes) / num_iterations for nodes in misplaced_frontier_nodes]
    misplaced_avg_process_times = [sum(times) / num_iterations for times in misplaced_process_times]

    # Calculate the error rates for process time
    manhattan_process_time_error = [100 * (time - manhattan_avg_process_times[i]) / manhattan_avg_process_times[i] for
                                    i, time in enumerate(manhattan_avg_process_times)]
    misplaced_process_time_error = [100 * (time - misplaced_avg_process_times[i]) / misplaced_avg_process_times[i] for
                                    i, time in enumerate(misplaced_avg_process_times)]

    manhattan_std_error = np.mean(manhattan_process_time_error)
    misplaced_std_error = np.mean(misplaced_process_time_error)

    # Plot the comparison between A* with Manhattan Distance and A* with Misplaced Tiles heuristics for all levels
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    x = np.arange(len(levels))
    rects1 = ax.bar(x - width / 2, manhattan_avg_costs, width, label='A* with Manhattan Distance')
    rects2 = ax.bar(x + width / 2, misplaced_avg_costs, width, label='A* with Misplaced Tiles')
    ax.set_ylabel('Cost')
    ax.set_title('Comparison between A* with Manhattan Distance and A* with Misplaced Tiles heuristics for all levels')
    ax.set_xticks(x)
    ax.set_xticklabels(['Level ' + str(level) for level in levels])
    ax.legend()

    # Show the plot
    plt.show()

    # Plot the average cost for each level and heuristic
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    x = np.arange(len(levels))
    rects1 = ax.bar(x - width / 2, manhattan_avg_costs, width, label='A* with Manhattan Distance')
    rects2 = ax.bar(x + width / 2, misplaced_avg_costs, width, label='A* with Misplaced Tiles')
    ax.set_ylabel('Cost')
    ax.set_title('Average Cost for A* with Manhattan Distance and A* with Misplaced Tiles heuristics for each level')
    ax.set_xticks(x)
    ax.set_xticklabels(['Level ' + str(level) for level in levels])
    ax.legend()

    # Show the plot
    plt.show()

    # Plot the average number of nodes expanded for each level and heuristic
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    x = np.arange(len(levels))
    rects1 = ax.bar(x - width / 2, manhattan_avg_nodes_expanded, width, label='A* with Manhattan Distance')
    rects2 = ax.bar(x + width / 2, misplaced_avg_nodes_expanded, width, label='A* with Misplaced Tiles')
    ax.set_ylabel('Number of Nodes Expanded')
    ax.set_title(
        'Average Number of Nodes Expanded for A* with Manhattan Distance and A* with Misplaced Tiles heuristics for each level')
    ax.set_xticks(x)
    ax.set_xticklabels(['Level ' + str(level) for level in levels])
    ax.legend()

    # Show the plot
    plt.show()

    # Plot the average number of frontier nodes for each level and heuristic
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    x = np.arange(len(levels))
    rects1 = ax.bar(x - width / 2, manhattan_avg_frontier_nodes, width, label='A* with Manhattan Distance')
    rects2 = ax.bar(x + width / 2, misplaced_avg_frontier_nodes, width, label='A* with Misplaced Tiles')
    ax.set_ylabel('Number of Frontier Nodes')
    ax.set_title(
        'Average Number of Frontier Nodes for A* with Manhattan Distance and A* with Misplaced Tiles heuristics for each level')
    ax.set_xticks(x)
    ax.set_xticklabels(['Level ' + str(level) for level in levels])
    ax.legend()

    # Show the plot
    plt.show()

    # Plot the average process time for each level and heuristic
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    x = np.arange(len(levels))
    rects1 = ax.bar(x - width / 2, manhattan_avg_process_times, width, label='A* with Manhattan Distance')
    rects2 = ax.bar(x + width / 2, misplaced_avg_process_times, width, label='A* with Misplaced Tiles')
    ax.set_ylabel('Process Time (s)')
    ax.set_title(
        'Average Process Time for A* with Manhattan Distance and A* with Misplaced Tiles heuristics for each level')
    ax.set_xticks(x)
    ax.set_xticklabels(['Level ' + str(level) for level in levels])
    ax.legend()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()