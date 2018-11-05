from abc import ABC, abstractmethod
from UserEntity import Player, Bank
from InputValidation import get_yes_or_no_input
from random import randint


class Location(ABC):
    """
    Abstract Parent Class for all locations on the board
    """

    @abstractmethod
    def __init__(self, location, name, price):
        self.location = location
        self.name = name
        self.price = price
        self.owner = Bank
        self.is_morgaged = False
        super().__init__()

    @abstractmethod
    def landed_on(self, player):
        pass

    def landed_on(self, player):
        """
        Returns the proper function depending on
        who landed on the property and who owns the property
        """
        if self.owner == Bank:
            self.owned_by_bank(player)
        elif self.owner != player:
            self.owned_by_player(player)

    def owned_by_bank(self, player):
        buy_or_pass = self.ask_buy_or_pass()
        if buy_or_pass:  # buy
            player.money = player.money - self.price
            self.owner = player
            player.owned_properites.update({self.location: self})
            self.is_morgaged = False
            self.price = self.price * 2

    def owned_by_player(self, player):
        self.owner.exchange_money(player, self.rent[self.number_of_houses])

    def ask_buy_or_pass(self):
        """
        asks the player if they would like to purchuse the
        property, and displays the Name and price
        """
        buy_or_pass = get_yes_or_no_input(
                            "Would you like to buy " + self.name +
                            "for $" + str(self.price) + "? y/n")
        return buy_or_pass

    def morgage(self):
        self.is_morgaged = True
        self.price = self.price / 2
        Bank.exchange_money(self, self.owner, self.price)
        self.owner = Bank

    def unmorgage(self, player):
        self.is_morgaged = False
        self.price = self.price * 2
        self.owner = player
        self.owner.exchange_money(self.owner, self.price * -.75)


class Property(Location):
    """
    Defines all the Properties on the board
    Does not include railroads or utilities
    """

    def __init__(self, location, property_data):
        """
        location: position on the board, int from 0 to 39
        property_data: list with vairous data formated as follows
        ["Name", Price, "Color", rent, rent_1_house, ..., rent_hotel]
        """
        self.color = property_data[2]
        self.rent = property_data[3:]
        self.number_of_houses = 0
        return super().__init__(location, property_data[0], property_data[1])


class Utility(Location):
    """
    Defines all utilities
    i.e. Electric Company and Water Works
    """

    def __init__(self, location, utility_data):
        """
        location: position on the board, int from 0 to 39
        utility_data: list with vairous data formated as follows
        ["Name", Price]
        """
        return super().__init__(location, utility_data[0], utility_data[1])

    def owned_by_player(self, player):
        num_utils_owned = 0
        multiplier = {1: 4, 2: 10}
        roll = randint(1, 6)
        for key in self.owner.owned_properites:
            if isinstance(self.owner.owned_properites[key], Utility):
                num_utils_owned += 1
        self.owner.exchange_money(player, roll * multiplier[num_utils_owned])


class Railroad(Location):
    """
    Defines all 4 railroads
    """

    def __init__(self, location, railraod_data):
        """
        location: position on the board, int from 0 to 39
        railroad_data: list with vairous data formated as follows
        ["Name", Price]
        """
        return super().__init__(location, railraod_data[0], railraod_data[1])

    def owned_by_player(self, player):
        num_railroads_owned = 0
        cost = {1: 50, 2: 100, 3: 150, 4: 200}
        for key in self.owner.owned_properites:
            if isinstance(self.owner.owned_properites[key], Railroad):
                num_railroads_owned += 1
        self.owner.exchange_money(player, cost[num_railroads_owned])
