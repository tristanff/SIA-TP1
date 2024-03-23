import time
from sokoban import initial_state, goal_test, generate_next_states, goal_state

def greedy():
    # WIP
    result = None
    return result

def main():
    # Measure the start time
    start_time = time.time()
    # Perform Greedy search
    result = greedy()
    # Measure the end time
    end_time = time.time()
    # Calculate the total time taken
    total_time = end_time - start_time
    
    if result is not None:
        print("Solution found:")
    else :
        print("No solution found")
    
if __name__ == "__main__":
    main()
