import time
import random
from sokoban import initial_state, goal_test, generate_next_states, goal_state, actions, action_function, print_state
import os


# Check if state would lead into a deadlock
def check_deadlock(state):

    # Check if point is a corner
    def is_corner(state, i, j):
        if (state[i - 1][j] == '#') and (state[i][j - 1] == '#'):
            return True
        elif (state[i - 1][j] == '#') and (state[i][j + 1] == '#'):
            return True
        elif (state[i + 1][j] == '#') and (state[i][j - 1] == '#'):
            return True
        elif (state[i + 1][j] == '#') and (state[i][j + 1] == '#'):
            return True
        return False

    # Check if point is a border
    def is_border(state, i, j):
        if (state[i - 1][j] == '#') or (state[i + 1][j]  == '#') or (state[i][j - 1] == '#') or (state[i][j + 1] == '#'):
            return True
        return False

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '*':
                if is_border(state, i, j):
                    # Box in corner = deadlock
                    if is_corner(state, i, j):
                        return True
                    else:
                        # Box on border between two corners = deadlock
                        if is_corner(state, i - 1, j) and is_corner(state, i + 1, j):
                            return True
                        if is_corner(state, i, j - 1) and is_corner(state, i, j + 1):
                            return True

                        # Neighboring boxes next to border = deadlock
                        if (state[i - 1][j] == '*') and is_border(state, i - 1, j):
                            return True
                        if (state[i][j - 1] == '*') and is_border(state, i, j - 1):
                            return True
                        if (state[i + 1][j] == '*') and is_border(state, i + 1, j):
                            return True
                        if (state[i][j + 1] == '*') and is_border(state, i, j + 1):
                            return True

            # Boxes stuck in this pattern:
            #       # # # #
            #       # . * .
            #       # * . .
            #       # . . .
            elif state[i][j] == '.' and is_corner(state, i, j):
                if (state[i - 1][j] == '#') and (state[i][j - 1] == '#') and (state[i + 1][j] == '*') and (state[i][j + 1] == '*'):
                    return True
                elif (state[i - 1][j] == '#') and (state[i][j + 1] == '#') and (state[i + 1][j] == '*') and (state[i][j - 1] == '*'):
                    return True
                elif (state[i + 1][j] == '#') and (state[i][j - 1] == '#') and (state[i - 1][j] == '*') and (state[i][j + 1] == '*'):
                    return True
                elif (state[i + 1][j] == '#') and (state[i][j + 1] == '#') and (state[i - 1][j] == '*') and (state[i][j - 1] == '*'):
                    return True

    # Otherwise, no deadlock
    return False


# Calculate Manhattan distance from one point to another
def manhattan_distance(state, goal_state, origin = '*', destination = '*'):
    distance = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == origin:
                box_pos = (i, j)
                target_pos = None
                # Find the closest target position
                for x in range(len(goal_state)):
                    for y in range(len(goal_state[x])):
                        if goal_state[x][y] == destination:
                            target_pos = (x, y)
                            break
                    if target_pos:
                        break
                distance += abs(box_pos[0] - target_pos[0]) + abs(box_pos[1] - target_pos[1])
    return distance

# Check if move playable
def playable(state, action):
    return not (state == action_function(state, action))


# Greedy search algorithm
def greedy(state, max_iter):

    # Initialize iteration count
    iteration = 0
    
    # Record step list
    steps = []
    
    # Search until goal reached or exceed iteration limit
    while not goal_test(state) and iteration < max_iter:
    
        # Print game state
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Step #{iteration + 1}")
        print_state(state)

        # Get possible moves
        next_states = generate_next_states(state)

        # Initialize variables to pick best action
        best_action = None
        heuristics = dict.fromkeys(actions)

        # Determine move based on lowest heuristic
        for action, next_state in zip(actions, next_states):
        
            # Verify if player can move and if move leads to known deadlock situation
            if playable(state, action) and not check_deadlock(next_state):
                heuristics[action] = manhattan_distance(next_state, goal_state, '*', '*') # manhattan_distance(next_state, next_state, '@', '*')

        # Heuristics scores (None = unplayable/deadlock)
        print("Heuristics:", heuristics)

        # Get minimum value keys
        min_value = min(value for value in heuristics.values() if value is not None)
        min_keys = [key for key, value in heuristics.items() if value == min_value]

        # Pick min heuristic and choose randomly if several moves have same value
        best_action = random.choice(min_keys)

        # Goal reached or no valid moves - end search
        if goal_test(state) or best_action == None:
            break

        # Update game state
        steps.append([state, heuristics]    )
        state = action_function(state, best_action)

        # Iteration count
        iteration += 1
        time.sleep(0.01)
    return state, steps


def main():
    # Measure the start time
    start_time = time.time()

    # Perform Greedy search
    state, steps = greedy(initial_state, 100)

    # Measure the end time
    end_time = time.time()

    # Calculate the total time taken
    total_time = end_time - start_time

    # Results
    print()
    print(f"Time elapsed: {round(total_time, 2)}s")
    print(f"Iterations: {len(steps)}")
    
    if goal_test(state):
        print("Solution found!")
    else:
        print("No solution found")
    
    reply = input("\nPrint step history? [y/n] ").lower()
    
    if reply == 'y':
        for i, step in enumerate(steps):
            print(f"\nStep {i+1}")
            print_state(step[0])
            print(step[1])

if __name__ == "__main__":
    main()
