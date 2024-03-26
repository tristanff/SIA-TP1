import time
import random
from sokoban import goal_test, actions, action_function, print_state, initial_state_level1, goal_state_level1, initial_state_level2, goal_state_level2, initial_state_level3, goal_state_level3
import os
import sys


# Count number of boxes on destination
def box_score(state, goal_state):
    count = 0
    for i in range(len(state)):
        for j in range(len(state[:])):
            if (state[i][j] == '*') and (goal_state[i][j] == '*'):
                count += 1
    return count

# Check if state would lead into a deadlock
def check_deadlock(state, next_state, goal_state):

    # Bypass check if action leads to goal state or new box on destination 
    if (next_state == goal_state) or (box_score(next_state, goal_state) > box_score(state, goal_state)):
        return False
    
    # Check if point is a corner
    def is_corner(next_state, i, j):
        if (next_state[i - 1][j] == '#') and (next_state[i][j - 1] == '#'):
            return True
        elif (next_state[i - 1][j] == '#') and (next_state[i][j + 1] == '#'):
            return True
        elif (next_state[i + 1][j] == '#') and (next_state[i][j - 1] == '#'):
            return True
        elif (next_state[i + 1][j] == '#') and (next_state[i][j + 1] == '#'):
            return True
        return False

    # Check if point is a border
    def is_border(next_state, i, j):
        if (next_state[i - 1][j] == '#') or (next_state[i + 1][j]  == '#') or (next_state[i][j - 1] == '#') or (next_state[i][j + 1] == '#'):
            return True
        return False

    # Iterate through all points on board
    for i in range(len(next_state)):
        for j in range(len(next_state[i])):
            if next_state[i][j] == '*':
                if is_border(next_state, i, j):
                    # Box in corner = deadlock
                    if is_corner(next_state, i, j) and (next_state[i][j] != '*'):
                        return True
                    else:
                        # Box on border between two corners = deadlock
                        if is_corner(next_state, i - 1, j) and is_corner(next_state, i + 1, j) and ((goal_state[i - 1][j] != '*') or (goal_state[i + 1][j] != '*')):
                            return True
                        elif is_corner(next_state, i, j - 1) and is_corner(next_state, i, j + 1) and ((goal_state[i][j - 1] != '*') and (goal_state[i][j + 1] != '*')):
                            return True

                        # Neighboring boxes next to border = deadlock
                        if (next_state[i - 1][j] == '*') and is_border(next_state, i - 1, j):
                            return True
                        elif (next_state[i][j - 1] == '*') and is_border(next_state, i, j - 1):
                            return True
                        elif (next_state[i + 1][j] == '*') and is_border(next_state, i + 1, j):
                            return True
                        elif (next_state[i][j + 1] == '*') and is_border(next_state, i, j + 1):
                            return True

            # Boxes stuck in this pattern:
            #       # # # #
            #       # . * .
            #       # * . .
            #       # . . .
            elif next_state[i][j] == '.' and is_corner(next_state, i, j):
                if (next_state[i - 1][j] == '#') and (next_state[i][j - 1] == '#') and (next_state[i + 1][j] == '*') and (next_state[i][j + 1] == '*'):
                    return True
                elif (next_state[i - 1][j] == '#') and (next_state[i][j + 1] == '#') and (next_state[i + 1][j] == '*') and (next_state[i][j - 1] == '*'):
                    return True
                elif (next_state[i + 1][j] == '#') and (next_state[i][j - 1] == '#') and (next_state[i - 1][j] == '*') and (next_state[i][j + 1] == '*'):
                    return True
                elif (next_state[i + 1][j] == '#') and (next_state[i][j + 1] == '#') and (next_state[i - 1][j] == '*') and (next_state[i][j - 1] == '*'):
                    return True

    # Otherwise, no deadlock
    return False


# Calculate Manhattan distance from one point to another
def manhattan_distance(state, goal_state):
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
            if state[i][j] != goal_state[i][j] and (state[i][j] != '#' or state[i][j] != '@'):
                heuristic += 1
    return heuristic


# Check if move playable
def playable(state, action):
    return not (state == action_function(state, action))


# Generate all possible next states (modified)
def generate_next_states(state):
    next_states = []
    for action in actions:
        new_state = action_function(state, action)
        next_states.append(new_state)
    return next_states


# Greedy search algorithm
def greedy(state, goal_state, max_iter):
    
    # Measure the start time
    start_time = time.time()

    # Initialize iteration count
    iteration = 0
    
    # Record step list
    steps = []
    
    # Search until goal reached or exceed iteration limit
    while not goal_test(state, goal_state) and iteration < max_iter:
        
        # Print game state
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Step #{iteration}")
        print_state(state)

        # Get possible moves
        next_states = generate_next_states(state)

        # Initialize variables to pick best action
        best_action = None
        heuristics = dict.fromkeys(actions)

        # Determine move based on lowest heuristic
        for action, next_state in zip(actions, next_states):
           
            # Verify if player can move and if move leads to known deadlock situation
            if playable(state, action) and not check_deadlock(state, next_state, goal_state):
                heuristics[action] = manhattan_distance(next_state, goal_state)

        # Heuristics scores (None = unplayable/deadlock)
        print("Heuristics:", heuristics)

        # Get minimum value keys
        min_value = min(value for value in heuristics.values() if value is not None)
        min_keys = [key for key, value in heuristics.items() if value == min_value]

        # Pick min heuristic and choose randomly if several moves have same value
        best_action = random.choice(min_keys)

        # Goal reached or no valid moves - end search
        if goal_test(state, goal_state) or best_action == None:
            break

        # Update game state
        steps.append([state, heuristics])
        state = action_function(state, best_action)
        
        # Iteration count
        iteration += 1
        
        #input()
        
    # Print game state
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Step #{iteration}")
    print_state(state)
    steps.append([state, "end"])
    
    # Measure the end time
    end_time = time.time()

    # Calculate the total time taken
    total_time = end_time - start_time
    
    return {
        'Status': ('Success' if goal_test(state, goal_state) else 'Failed'),
        'State': state,
        'Cost': iteration,
        'Solution': (state if goal_test(state, goal_state) else None),
        'ProcessTime': round(total_time, 2),
        'Steps': steps
    }


def main():
    
    # Levels to load
    levels = {'1': [initial_state_level1, goal_state_level1], \
              '2': [initial_state_level2, goal_state_level2], \
              '3': [initial_state_level3, goal_state_level3]}
    
    # Check if level was entered 
    if sys.argv[1] not in levels.keys():
        print("Please enter a valid level")
    
    # Run algorithm
    else:
    
        # Retrieve level requested by user
        initial_state = levels[sys.argv[1]][0]
        goal_state = levels[sys.argv[1]][1]

        # Perform Greedy search
        result = greedy(initial_state, goal_state, 1000)

        # Results
        print(f"Time elapsed: {result['ProcessTime']}s")
        print(f"Iterations: {result['Cost']}")
          
        if goal_test(result['State'], goal_state):
            print("Solution found!")
        else:
            print("No solution found")
        
        reply = input("\nPrint step history? [y/n] ").lower()
        
        if reply in ['y', ''] :
            for i, step in enumerate(result['Steps']):
                print(f"\nStep {i+1}")
                print_state(step[0])
                print(step[1])

if __name__ == "__main__":
    main()
