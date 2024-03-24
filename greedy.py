import time
import random
from sokoban import initial_state, goal_test, generate_next_states, goal_state, actions, action_function, print_state

def manhattan_distance(state):
    distance = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '*':
                box_pos = (i, j)
                target_pos = None
                # Find the closest target position
                for x in range(len(goal_state)):
                    for y in range(len(goal_state[x])):
                        if goal_state[x][y] == '.':
                            target_pos = (x, y)
                            break
                    if target_pos:
                        break
                distance += abs(box_pos[0] - target_pos[0]) + abs(box_pos[1] - target_pos[1])
    return distance

# Greedy search algorithm
def greedy(state):
    i = 0
    while True:
        # Print game state
        print("\t game state")
        print_state(state)
        
        # Get possible moves
        next_states = generate_next_states(state)
        
        # Infinitely large value to initialize min
        min_heuristic = float('inf')
        best_action = None
        
        heuristics = dict.fromkeys(actions)
        
        # Determine move based on lowest heuristic
        for action, next_state in zip(actions, next_states):
            heuristics[action] = manhattan_distance(next_state)
            print(action)
            
        print(heuristics)
            
        # Get minimum value keys
        min_value = min(value for value in heuristics.values() if value is not None)
        min_keys = [key for key, value in heuristics.items() if value == min_value]
        
        # Pick min heuristic and choose randomly if several moves have same value
        best_action = random.choice(min_keys)
            
        # Goal reached or no valid moves - end search
        if goal_test(state) or best_action == None:
            break
        
        # Update game state
        state = action_function(state, best_action)
    return state

def main():
    # Measure the start time
    start_time = time.time()
    
    # Perform Greedy search
    state = greedy(initial_state)
    
    # Measure the end time
    end_time = time.time()
    
    # Calculate the total time taken
    total_time = end_time - start_time
    
    if goal_test(state):
        print("Solution found!")
    else :
        print("No solution found")
    
if __name__ == "__main__":
    main()
