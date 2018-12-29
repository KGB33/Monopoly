def get_yes_or_no_input(prompt):
    """
    Prompts the user for a y/n answer
    returns True if yes, and False if no

    :param prompt: (String)
        prompt for input.

    :return: (Boolean)
        True for Yes
        False for No
    """
    while True:
        value = input(prompt + " [y/n]: ")
        if value == 'y':
            return True
        elif value == 'n':
            return False
        else:
            print("Input not accepted, please try again\n")


def get_positive_non_zero_int_input(prompt):
    """
    Prompts the user for a positive int input

    :param prompt: (String)
        Prompts user for input

    :return: (int)
        a positive, non-zero int
    """
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Input must be positive, try again.")
        except ValueError:
            print("Input must be numeric")
