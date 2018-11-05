def get_yes_or_no_input(prompt):
    """
    prompts the user for a y/n answer
    returns True if yes, and False if no
    """
    while True:
        value = input(prompt + " [y/n]: ")
        if value == 'y':
            return True
        elif value == 'n':
            return False
        else:
            print("Input not accepted, please try again\n")
