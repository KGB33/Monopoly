from abc import ABC, abstractmethod
from UserEntity import Player, Bank, FreeParking
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

    def __init__(self, location, name, price=150):
        """
        location: position on the board, int from 0 to 39
        price defalut = 150
        """
        return super().__init__(location, name, price)

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

    def __init__(self, location, name, price=200):
        """
        location: position on the board, int from 0 to 39
        railroad_data: list with vairous data formated as follows
        ["Name", Price]
        """
        return super().__init__(location, name, price)

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
        pass

    def advance_to_tile(self, tile_num):
        """
        Moves player to specified tile
        """
        # Checks if player will pass go
        if self.active_player.position >= tile_num:
            self.active_player.money += 200
        self.active_player.position = tile_num
        return Board.spaces[self.active_player.position].landed_on(self.active_player)

    def advance_to_next(self, class_type):
        location_to_check = self.active_player.position + 1
        passed_go = False
        while not isinstance(
            Board.spaces[location_to_check], class_type):
            location_to_check += 1
            if location_to_check > 39:
                location_to_check = location_to_check % 40
                passed_go = True
        self.active_player.position = location_to_check
        if passed_go:
            self.active_player.money += 200
        return Board.spaces[self.active_player.position].landed_on(self.active_player)

    def gain_money(self, amount):
        self.active_player.money += amount

    def lose_money(self, amount):
        Board.spaces[20].exchange_money(self.active_player, amount)

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
        Board.spaces[20].exchange_money(self.active_player, owed_money)

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
        key = randint(0,16)
        if key == 0:
            return self.advance_to_tile(0)
        elif key == 1:
            return self.advance_to_tile(24)
        elif key == 2:
            return self.advance_to_tile(11)
        elif key == 3:
            return self.advance_to_next(Utility)
        elif key == 4:
            return self.advance_to_next(Railroad)
        elif key == 5:
            return self.advance_to_next(Railroad)
        elif key == 6:
            return self.gain_money(50)
        elif key == 7:
            self.get_out_of_jail_free()
        elif key == 8:
            return self.go_back(3)
        elif key == 9:
            return self.go_to_jail()
        elif key == 10:
            return self.house_repairs()
        elif key == 11:
            return self.lose_money(15)
        elif key == 12:
            return self.advance_to_tile(5)
        elif key == 13:
            return self.advance_to_tile(39)
        elif key == 14:
            return self.pay_all_other_players(50)
        elif key == 15:
            return self.gain_money(150)
        elif key == 16:
            return self.gain_money(100)
        else:
            return print("Bad Chance Card Draw")
    

class CommunityChest(Card):
    """
    All Community Chest Cards
    """

    def __init__(self, location, name):
        return super().__init__(location, name)

    def draw_card(self):
        key = randint(0,16)
        if key == 0:
            return self.advance_to_tile(0)
        elif key == 1:
            return self.gain_money(200)
        elif key == 2:
            return self.lose_money(50)
        elif key == 3:
            return self.gain_money(50)
        elif key == 4:
            return self.get_out_of_jail()
        elif key == 5:
            return self.go_to_jail()
        elif key == 6:
            return self.get_money_from_all_other_players(50)
        elif key == 7:
            return self.gain_money(100)
        elif key == 8:
            return self.gain_money(20)
        elif key == 9:
            return self.get_money_from_all_other_players(10)
        elif key == 10:
            return self.gain_money(100)
        elif key == 11:
            return self.lose_money(50)
        elif key == 12:
            return self.lose_money(150)
        elif key == 13:
            return self.gain_money(25)
        elif key == 14:
            return self.house_repairs()
        elif key == 15:
            return self.gain_money(10)
        elif key == 16:
            return self.gain_money(100)
        else:
            print("bad CC draw")


class Board(object):
    """
    The Monopoly Board
    Using temp spaces dictionary for testing
    """
    spaces = {}
    streets = { x: Property(x, ["Name", 150, "Color", 5, 10, 20, 40, 80, 160])
                for x in range(0, 40)}
    railroads = {x: Railroad(x, "Name") for x in [5, 15, 25, 35]}
    utilitys = {x: Utility(x, "Name") for x in [12, 28]}
    chances = {x: Chance(x, "Chance Card") for x in [7, 22, 36]}
    community_chest = {x: CommunityChest(x, "Community Chest Card")
                        for x in [2, 17, 33]}
    free_parking = {20: FreeParking()}
    spaces.update(streets)
    spaces.update(railroads)
    spaces.update(utilitys)
    spaces.update(chances)
    spaces.update(community_chest)
    spaces.update(free_parking)
    