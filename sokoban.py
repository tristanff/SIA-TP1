# définir l'état initial du jeu
initial_state = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '@', '*', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '#', '#', '#', '#', '#', '#']
]

# définir l'état final du jeu
goal_state = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '@', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '*', '#'],
    ['#', '#', '#', '#', '#', '#', '#']
]

# définir les actions possibles
actions = ['up', 'down', 'left', 'right']

# définir la fonction d'action
def action_function(state, action):
    # créer une copie de l'état courant
    new_state = [row[:] for row in state]

    # obtenir la position actuelle du joueur
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '@':
                player_pos = (i, j)

    # calculer la nouvelle position du joueur
    new_player_pos = None
    if action == 'up':
        new_player_pos = (player_pos[0] - 1, player_pos[1])
    elif action == 'down':
        new_player_pos = (player_pos[0] + 1, player_pos[1])
    elif action == 'left':
        new_player_pos = (player_pos[0], player_pos[1] - 1)
    elif action == 'right':
        new_player_pos = (player_pos[0], player_pos[1] + 1)

    # vérifier si la nouvelle position est valide
    if new_player_pos is not None and new_state[new_player_pos[0]][new_player_pos[1]] != '#':
        # vérifier s'il y a une caisse à la nouvelle position
        if new_state[new_player_pos[0]][new_player_pos[1]] == '.':
            # déplacer le joueur à la nouvelle position
            new_state[new_player_pos[0]][new_player_pos[1]] = '@'
            new_state[player_pos[0]][player_pos[1]] = '.'
        elif new_state[new_player_pos[0]][new_player_pos[1]] == '*':
            # vérifier si la caisse peut être poussée
            new_box_pos = (new_player_pos[0] + (-1 if action == 'up' else 1), new_player_pos[1] + (-1 if action == 'left' else 1))
            if new_state[new_box_pos[0]][new_box_pos[1]] == '.':
                # déplacer la caisse à la nouvelle position
                new_state[new_box_pos[0]][new_box_pos[1]] = '*'
                new_state[new_player_pos[0]][new_player_pos[1]] = '.'
                # déplacer le joueur à la nouvelle position
                new_state[new_player_pos[0]][new_player_pos[1]] = '@'
                new_state[player_pos[0]][player_pos[1]] = '.'

    # retourner le nouvel état
    return new_state

# définir la fonction de test de but
def goal_test(state):
    # vérifier si toutes les caisses sont à leurs positions cibles
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '*' and goal_state[i][j] == '.':
                return False
            elif state[i][j] == '.' and goal_state[i][j] == '*':
                return False
    return True

# définir la fonction pour générer tous les états suivants possibles
def generate_next_states(state):
    next_states = []
    for action in actions:
        new_state = action_function(state, action)
        if new_state not in next_states:
            next_states.append(new_state)
    return next_states

