import os
from sokoban import *
def main():
    state = initial_state_level2
    while True:
        os.system('clear')  # clear the console
        print_state(state)  # print the current state
        action = get_user_action()  # get the user action from the keyboard
        state = action_function(state, action)  # update the state with the new action
        if goal_test(initial_state_level2,goal_state_level2):  # check if the game is won
            os.system('clear')
            print_state(state)
            print("You win!")
            break

if __name__ == "__main__":
    main()
