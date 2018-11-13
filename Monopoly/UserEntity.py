from random import randint
from Exceptions import PlayerInJailError
from InputValidation import get_yes_or_no_input
from abc import ABC, abstractmethod


class UserEntity(ABC):
    """
    Abstract base class for Player and Bank Classes
    """
    def __init__(self, money_in=0):
        self.money = money_in

    def exchange_money(self, paying_player, amount):
        """
        Takes money from paying_player and gives to self
        """
        self.money += amount
        paying_player.money -= amount


class Player(UserEntity):
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
        self.get_out_of_jail_cards = 0
        return super().__init__(money_in=money_in)

    def roll_dice(self, num_doubles=0):
        """
        rolls 2 d6's, adds them to the player's position,
        checks for doubles, then runs the landed on method
        if doubles are rolled, roll again if not in jail
        """
        dice_1 = randint(1, 6)
        dice_2 = randint(1, 6)
        try:
            if dice_1 == dice_2:
                # doubles rolled
                num_doubles = num_doubles + 1
            if num_doubles == 3:
                # go to jail
                self.position = 'jail'
                # call landed on
            else:
                if self.position == 'jail':
                    raise PlayerInJailError
                self.move_player(dice_1 + dice_2)
                # Call landed on
                if dice_1 == dice_2:
                    return self.roll_dice(num_doubles=num_doubles)
        except PlayerInJailError:
            use_card = False
            pay_bail = False
            if self.get_out_of_jail_cards > 0:
                use_card = get_yes_or_no_input(
                    "Would you like you use a get out of free card? you have"
                    + str(get_out_of_jail_cards))
            else:
                pay_bail = get_yes_or_no_input("Would you like to pay bail? ($50)")
            if use_card:
                self.position = 10
                self.move_player(dice_1 + dice_2)
            if pay_bail:
                self.money -= 50
                self.position = 10
                self.move_player(dice_1 + dice_2)
            if num_doubles == 1:
                self.position = 10
                self.move_player(dice_1 + dice_2)
                return self.roll_dice(num_doubles=num_doubles)

    def move_player(self, num_spaces):
        self.position += num_spaces
        if self.position > 39:  # pass go, get money
            self.money += 200
        self.position = self.position % 40

    def landed_on(self):
        """
        WIP
        Checks with the board object to determan what was
        landed on, and then activeates the property's method
        """
        return self.position


class Bank(UserEntity):
    """
    The Bank Class for the game
    """
    def __init__(self, money_in=0):
        return super().__init__(money_in=money_in)

    def exchange_money(self, paying_player, amount):
        """
        Takes money from paying player
        """
        paying_player.money -= amount

class FreeParking(UserEntity):
    def __init__(self, money_in = 0):
        return super().__init__(money_in)
