from abc import ABC, abstractmethod
from UserEntity import Player, Bank
from InputValidation import get_yes_or_no_input

class Location(ABC):
    """
    Abstract Parent Class for all locations on the board
    """

    @abstractmethod
    def __init__(self, location_in):
        self.location = location_in
        super().__init__()

    @abstractmethod
    def landed_on(self, player):
        pass



class Property(Location):
    """
    Defines all the Properties on the board
    Does not include railroads or utilities
    """

    def __init__(self, location_in, property_data_in):
        """
        location: position on the board, int from 0 to 39
        property_data_in: list with vairous data formated as follows
        ["Name", "Color", Price, rent, rent_1_house, ..., rent_hotel]
        """
        super().__init__(location_in)
        self.name = property_data_in[0]
        self.color = property_data_in[1]
        self.price = property_data_in[2]
        self.rent = property_data_in[3:]
        self.number_of_houses = 0
        self.owner = Bank
        self.is_morgaged = False
        

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
        if buy_or_pass: #buy
            player.money = player.money - self.price
            self.owner = player
            player.owned_properites.update({self.location : self.name})
            self.is_morgaged = False
            self.price = self.price * 2

    def owned_by_player(self, player):
        self.owner.money += self.rent[self.number_of_houses]
        player.money -= self.rent[self.number_of_houses]

    def ask_buy_or_pass(self):
        """
        asks the player if they would like to purchuse the
        property, and displays the Name and price
        """
        buy_or_pass = get_yes_or_no_input("Would you like to buy " + self.name +
                                    "for $" + str(self.price) + "? y/n")
        return buy_or_pass

    def morgage(self):
        self.is_morgaged = True
        self.price = self.price / 2
        self.owner.money += self.price
        self.owner = Bank

    def unmorgage(self, player):
        self.is_morgaged = False
        self.price = self.price * 2
        self.owner = player
        self.owner.money -= self.price * .75