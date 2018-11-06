from abc import ABC, abstractmethod
from UserEntity import Player, Bank
from InputValidation import get_yes_or_no_input
from random import randint

class Board(object):
    """
    The Monopoly Board
    Using temp spaces dictionary for testing
    """
    def __init__(self):
        self.spaces = { x: Property(x, ["Name", 150, "Color", 5, 10, 20, 40, 80, 160])
                  for x in range(0, 40)}


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


class Effect(ABC):
    """
    Parent class for all squares where an effect is
    appled. Including Chance, Community Chest, Income tax, etc.
    """

    @abstractmethod
    def __init__(self, location, name):
        self.location = location
        self.name = name

    @abstractmethod
    def landed_on(self, player):
        pass


class Card(Effect):
    """
    Parent Class for Chance and Communty Chest Cards
    """

    def __init__(self, location, name):
        self.active_player = Player
        return super().__init__(location, name)

    def landed_on(self, player):
        self.active_player = player
        return self.draw_card()

    def draw_card(self):
        cards = {0: "Cards not implemented."}
        return cards[randint(0, len(cards) - 1)]

    def advance_to_tile(self, tile_num):
        """
        Moves player to specified tile
        """
        # Checks if player will pass go
        if self.active_player.position >= tile_num:
            self.active_player.money += 200
        self.active_player.position = tile_num
        return Board[self.active_player.position].landed_on()

    def advance_to_next(self, class_type):
        i = 0
        while True:
            if isinstance(Board[self.active_player.position + i], class_type):
                self.active_player.position += i
                if self.active_player.position >= 40:
                    self.active_player.money += 200
                    self.active_player.position = self.active_player.position % 40
                return Board[self.active_player.position].landed_on
            else:
                i += 1

    def gain_money(self, amount):
        self.active_player.money += amount

    def lose_money(self, amount):
        FreeParking.pay_money(amount)

    def get_out_of_jail_free(self):
        self.active_player.get_out_of_jail_cards += 1

    def go_back(self, num_tiles):
        self.active_player.position -= num_tiles
        return Board[self.active_player.position].landed_on()

    def go_to_jail(self):
        self.active_player.position = 'jail'

    def house_repairs(self):
        owed_money = 0
        for key in self.active_player.owned_properties:
            hold = self.active_player.owned_properties[key].number_of_houses
            owed_money += 25 * hold
        FreeParking.pay_money(owed_money, self.active_player)

    def pay_all_other_players(self, amount):
        for person in game:
            person.exchange_money(self.active_player, amount)

    def get_money_from_all_other_players(self, amount):
        self.pay_all_other_self.active_players(-1 * amount)
          

class Chance(Card):
    """
    All Chance Cards
    """

    def __init__(self, location, name):
        return super().__init__(location, name)

    def draw_card(self):
        cards = {
            0: self.advance_to_tile(0),
            1: self.advance_to_tile(24),
            2: self.advance_to_tile(11),
            3: self.advance_to_next(Utility),
            4: self.advance_to_next(Railroad),
            5: self.advance_to_next(Railroad),
            6: self.gain_money(50),
            7: self.get_out_of_jail_free(),
            8: self.go_back(3),
            9: self.go_to_jail(),
            10: self.house_repairs(),
            11: self.lose_money(15),
            12: self.advance_to_tile(5),
            13: self.advance_to_tile(39),
            14: self.pay_all_other_players(50),
            15: self.gain_money(150),
            16: self.gain_money(100)}
        return cards[randint(0, len(cards) - 1)]

    

class CommunityChest(Card):
    """
    All Community Chest Cards
    """
    def __init__(self, location, name):
        return super().__init__(location, name)

    def draw_card(self):
        cards = {
            0: self.self.advance_to_tile(0),
            1: self.gain_money(200),
            2: self.lose_money(50),
            3: self.gain_money(50),
            4: self.get_out_of_jail(),
            5: self.go_to_jail(),
            6: self.get_money_from_all_other_players(50),
            7: self.gain_money(100),
            8: self.gain_money(20),
            9: self.get_money_from_all_other_players(10),
            10: self.gain_money(100),
            11: self.lose_money(50),
            12: self.lose_money(150),
            13: self.gain_money(25),
            14: self.house_repairs(),
            15: self.gain_money(10),
            16: self.gain_money(100)}
        return cards[randint(0, len(cards) - 1)]
