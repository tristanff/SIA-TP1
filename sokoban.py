# define initial state of the game
initial_state = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '*', '.', '.', '.', '#'],
    ['#', '@', '.', '.', '.', '.', '#'],
    ['#', '#', '#', '#', '#', '#', '#']
]

# define goal state of the game
goal_state = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '@', '.', '.', '.', '*', '#'],
    ['#', '#', '#', '#', '#', '#', '#']
]

# define possible actions
actions = ['up', 'down', 'left', 'right']

# define action function
def action_function(state, action):
    # create a copy of the current state
    new_state = [row[:] for row in state]

    # get the current player position
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '@':
                player_pos = (i, j)

    # calculate the new player position
    new_player_pos = None
    if action == 'up':
        new_player_pos = (player_pos[0] - 1, player_pos[1])
    elif action == 'down':
        new_player_pos = (player_pos[0] + 1, player_pos[1])
    elif action == 'left':
        new_player_pos = (player_pos[0], player_pos[1] - 1)
    elif action == 'right':
        new_player_pos = (player_pos[0], player_pos[1] + 1)

    # check if the new position is valid
    if new_player_pos is not None and new_state[new_player_pos[0]][new_player_pos[1]] != '#':
        # check if there is a box at the new position
        if new_state[new_player_pos[0]][new_player_pos[1]] == '.':
            # move the player to the new position
            new_state[new_player_pos[0]][new_player_pos[1]] = '@'
            new_state[player_pos[0]][player_pos[1]] = '.'
        elif new_state[new_player_pos[0]][new_player_pos[1]] == '*':
            # check if the box can be pushed
            if action == 'up':
                new_box_pos = (new_player_pos[0] -1 , new_player_pos[1])
            elif action == 'down':
                new_box_pos = (new_player_pos[0] + 1 , new_player_pos[1])
            elif action == 'left':
                new_box_pos = (new_player_pos[0], new_player_pos[1] - 1)
            elif action == 'right':
                new_box_pos = (new_player_pos[0], new_player_pos[1] + 1)
            if new_state[new_box_pos[0]][new_box_pos[1]] == '.':
                # move the box to the new position
                new_state[new_box_pos[0]][new_box_pos[1]] = '*'
                # move the player to the new position
                new_state[new_player_pos[0]][new_player_pos[1]] = '@'
                new_state[player_pos[0]][player_pos[1]] = '.'

    # return the new state
    return new_state

# define goal test function
def goal_test(state):
    # check if all boxes are at their target positions
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '*' and goal_state[i][j] == '.':
                return False
            elif state[i][j] == '.' and goal_state[i][j] == '*':
                return False
    return True

# define function to generate all possible next states
def generate_next_states(state):
    next_states = []
    for action in actions:
        new_state = action_function(state, action)
        if new_state not in next_states:
            next_states.append(new_state)
    return next_states