import os
from sokoban import initial_state,print_state,get_user_action,action_function,goal_test
def main():
    state = initial_state
    while True:
        os.system('clear')  # clear the console
        print_state(state)  # print the current state
        action = get_user_action()  # get the user action from the keyboard
        state = action_function(state, action)  # update the state with the new action
        if goal_test(state):  # check if the game is won
            os.system('clear')
            print_state(state)
            print("You win!")
            break

if __name__ == "__main__":
    main()
