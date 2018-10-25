from random import randint
from Board import Board


class Player:
    """
    Holds player data: Money, propteries owned, ect.

    methods are responceable for player actions
        i.e. rolling dice, buying houses, paying rent, ect.
    """

    STARTING_MONEY = 1500

    def __init__(self, name_in, money_in=STARTING_MONEY):
        """
        Default Starting Money is $1,500
        """
        self.name = name_in
        self.position = 0
        self.owned_properites = {}
        self.money = money_in

    def roll_dice(self, num_doubles=0):
        """
        rolls 2 d6's, adds them to the player's position,
        checks for doubles, then runs the landed on method
        if doubles are rolled, roll again if not in jail
        """
        dice_1 = randint(1, 6)
        dice_2 = randint(1, 6)
        if dice_1 == dice_2:
            # doubles rolled
            num_doubles = num_doubles + 1
        if num_doubles == 3:
            # go to jail
            self.position = 'jail'
            # call landed on
        else:
            self.position = self.position + dice_1 + dice_2
            self.position = self.position % 40
            # Call landed on
            if dice_1 == dice_2:
                return self.roll_dice(num_doubles=num_doubles)

    def landed_on(self):
        """
        WIP
        Checks with the board object to determan what was
        landed on, and then activeates the property's method
        """
        return Board.spaces[self.position]
