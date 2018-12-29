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

    def __str__(self):
        output = "This UserEntity has ${0}".format(self.money)
        return output


class Player(UserEntity):
    """
    Holds player data: Money, properties owned, ect.

    methods are replaceable for player actions
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
        super().__init__(money_in=money_in)

    def roll_dice(self, num_doubles=0):
        """
        rolls 2 d6's, adds them to the player's position,
        checks for doubles, then runs the landed on method
        if doubles are rolled, roll again if not in jail
        """
        dice_1 = randint(1, 6)
        dice_2 = randint(1, 6)
        print("You Rolled: (", dice_1, ",", dice_2, ")!",
              "\nFor a total of:", dice_1 + dice_2)
        try:
            if dice_1 == dice_2:
                print("Doubles! Awesome!!")
                num_doubles = num_doubles + 1
            else:
                num_doubles = 0
            if self.position == 'jail':
                raise PlayerInJailError
            if num_doubles == 3:
                # go to jail
                self.position = 'jail'
                print("You rolled too many doubles and landed in jail")
                return num_doubles
            else:
                self.move_player(dice_1 + dice_2)
                return num_doubles
        except PlayerInJailError:
            use_card = False
            pay_bail = False
            if self.get_out_of_jail_cards > 0:
                use_card = get_yes_or_no_input(
                    "Would you like you use a get out of free card? you have"
                    + str(self.get_out_of_jail_cards))
            else:
                pay_bail = get_yes_or_no_input("Would you like to pay bail? ($50)")
            if use_card:
                self.position = 10
                self.move_player(dice_1 + dice_2)
                return num_doubles
            if pay_bail:
                self.money -= 50
                self.position = 10
                self.move_player(dice_1 + dice_2)
                return num_doubles
            if num_doubles != 0:
                self.position = 10
                self.move_player(dice_1 + dice_2)
                return num_doubles

    def move_player(self, num_spaces):
        self.position += num_spaces
        if self.position > 39:  # pass go, get money
            self.money += 200
        self.position = self.position % 40

    @staticmethod
    def turn_options():
        """
        Possible Options:
            Roll Dice
            Buy Houses
            View Properties
        """
        while True:
            choice = input('\tWhat would you like to do?'
                           '\n\t\t(r) Roll Dice'
                           '\n\t\t(b) Buy Houses/Hotels'
                           '\n\t\t(v) View Owned Properties'
                           '\n>>>').lower()
            if choice == 'r':
                return 'r'
            elif choice == 'b':
                print('TODO')  # TODO: Add buy houses method
                return 'b'
            elif choice == 'v':
                print('TODO, view owned properties')  # TODO: Add method to view properties
                return 'v'
            else:
                print("Input not recognised, please try again\n")

    def __str__(self):
        output = "{0}\t${1}" \
                 "\n\tIs On {2}".format(self.name, self.money, self.position)
        return output


class Bank(object):
    """
    The Bank Class for the game
    """

    @staticmethod
    def exchange_money(paying_player, amount):
        """
        Takes money from paying player
        """
        paying_player.money -= amount

    @classmethod
    def __str__(cls):
        output = "The Bank"
        return output


class FreeParking(UserEntity):
    """
    Free parking space
    """

    def __init__(self, money_in=0):
        self.name = "Free Parking"
        super().__init__(money_in)

    def landed_on(self, player):
        player.money += self.money
        self.money = 0

    def __str__(self):
        output = "20 {0}" \
                 "\n\tThere is ${1} up for grabs".format(self.name, self.money)
        return output
